## Hadoop
Hadoop jceks file

`hadoop credential create password.alias -value PASSwordvalue -provider jceks://hdfs/tmp/test.jceks`

`hadoop credential create password.alias -provider jceks://hdfs/tmp/test.jceks` - This option is more secure, terminal will ask a password.

Get jceks password as string.

`
import org.apache.hadoop.security.alias.CredentialProviderFactory

val conf = new org.apache.hadoop.conf.Configuration()

val alias = "password.alias"

val jceksPath = "jceks://hdfs/tmp/test.jceks"

conf.set(CredentialProviderFactory.CREDENTIAL_PROVIDER_PATH, jceksPath)

val sqoopPwd = conf.getPassword(alias).mkString
`


**Hadoop and S3**

There are some issues with hadoop, spark and S3 that we need to bear in mind when working with it.

**Issues**: 

**S3 secret key with slash.**
Change the aws secret key and generate one without slash.

**S3 bucket name with dots.**
https://docs.aws.amazon.com/AmazonS3/latest/dev/BucketRestrictions.html
For best compatibility, we recommend that you avoid using dots (.) in bucket names


**S3 files/path with = or spaces.**
Remove these specials chars inside the path or file name.

**Parquet files being write only in region eu-west-1(Ireland)**
https://hadoop.apache.org/docs/r3.1.2/hadoop-aws/tools/hadoop-aws/troubleshooting_s3a.html#a.E2.80.9CBad_Request.E2.80.9D_exception_when_working_with_AWS_S3_Frankfurt.2C_Seoul.2C_or_other_.E2.80.9CV4.E2.80.9D_endpoint

S3 Frankfurt and Seoul only support the V4 authentication API.

Requests using the V2 API will be rejected with 400 Bad Request
https://stackoverflow.com/questions/36647087/using-s3-frankfurt-with-spark

`
System.setProperty("com.amazonaws.services.s3.enableV4", "true")
hadoopConf.set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
hadoopConf.set("com.amazonaws.services.s3.enableV4", "true")
hadoopConf.set("fs.s3a.endpoint", "s3." + region + ".amazonaws.com")
`


**Hadoop distcp to S3**

`
hadoop distcp \
  -Dfs.s3a.access.key=your_access_key \
  -Dfs.s3a.secret.key=your_secret_key \
  -Dfs.s3a.fast.upload=true \
  /yourpath/something.parquet s3a://bucket-name/path/ 
`

`
hadoop distcp \
  -Dfs.s3a.access.key=your_access_key \
  -Dfs.s3a.secret.key=your_secret_key \
  -Dfs.s3a.fast.upload=true \
  /yourpath/something.parquet s3a://bucket-name/path/custom_name.parquet 
`


## Impala

Adding a new column into a nested field (Struct). This also could be used to change the type or name of the fields, it recreates the nested structure again with the new values.

`
ALTER TABLE db.table_name 
CHANGE column column STRUCT<column1:STRUCT<final_column:STRING>>
`



## Spark
Force caching and checking if the dataframe was cached
https://medium.com/@gaga19900329/force-caching-spark-dataframes-84d32730a21

when and why cache a dataframe
https://stackoverflow.com/questions/44156365/when-to-cache-a-dataframe

## Hive
  Serialization Encoding
    ALTER TABLE  schema.table SET SERDEPROPERTIES ('serialization.encoding'='ISO-8859-1');
    ALTER TABLE  schema.table SET SERDEPROPERTIES ('serialization.encoding'='UTF-8');
    TBLPROPERTIES ( 'store.charset'='ISO-8859-1', 
      'retrieve.charset'='ISO-8859-1');
  
  Update metadata partition
    MSCK REPAIR TABLE <tablename>;
  
  Load Data
  
  load data inpath 'hdfs_path' into  schema.table;
  load data local inpath 'local_path' overwrite into table categories;
  
  Create table as another
  
  CREATE TABLE yourtable
  LIKE table2;

  
Map Reduce queue
set mapred.job.queue.name=root.abc;

## Iconv

iconv --from-code=UTF-8 --to-code=ISO-8859-1 utf8_tst.csv > iso88591_tst.csv
iconv --from-code=UTF-8 --to-code=ascii//TRANSLIT with_special_char.csv > without_special_char.csv
https://www.tecmint.com/convert-files-to-utf-8-encoding-in-linux/


## Pandas

read csv and change Nan to null for string reading.
df = pandas.read_csv(csv_file, sep=';', lineterminator='\n', error_bad_lines=False, keep_default_na=False)


Linux proc view output
ps -eaf | grep something
tail -f /proc/<pid>/fd/1
1 = stdout, 2 = stderr


## Apache Airflow

**Airflow 1.8 update** - **Bitshift Composition**

Traditionally, operator relationships are set with the set_upstream() and set_downstream() methods. In Airflow 1.8, this can be done with the Python **bitshift operators** >> and <<. The following four statements are all functionally equivalent:

`op1 >> op2
op1.set_downstream(op2)

op2 << op1
op2.set_upstream(op1)`

TemplateNotFound error when running simple Airflow BashOperator
https://stackoverflow.com/questions/42147514/templatenotfound-error-when-running-simple-airflow-bashoperator
https://cwiki.apache.org/confluence/display/AIRFLOW/Common+Pitfalls

Airflow tricks
https://medium.com/datareply/airflow-lesser-known-tips-tricks-and-best-practises-cf4d4a90f8f

## Big Query

**Strongly avoid run functions or parse in a partition_date field**, it may cause a Full Scan on the table.

select * from dataset.table t
where format_date('%Y%m%d', t.partition_date) = '20190618' --- 4.6TB


Change the function or parse to the value not on the partition field. 

select * from dataset.table t
where t.partition_date = PARSE_DATE('%Y%m%d', '20190618') ---87GB


**Loop replicating data to other range of data**
https://stackoverflow.com/questions/54481850/do-loop-in-bigquery

#standardSQL
WITH `project.dataset.table` AS (
  SELECT 'TV' Type, '20180101' Start_Date, '20180131' End_Date, 10000 Total_Spend UNION ALL
  SELECT 'Radio', '20180107', '20180207', 5000 
)
SELECT type, FORMAT_DATE('%Y%m%d', day) day, 
  ROUND(Total_Spend / ARRAY_LENGTH(GENERATE_DATE_ARRAY(PARSE_DATE('%Y%m%d', Start_Date), PARSE_DATE('%Y%m%d', End_Date))), 2) Spend
FROM `project.dataset.table`, UNNEST(GENERATE_DATE_ARRAY(PARSE_DATE('%Y%m%d', Start_Date), PARSE_DATE('%Y%m%d', End_Date))) day
-- ORDER BY Type, day

**Select all except nested column or specific field inside the nested field**

Exemple of select * except a nested column payload
SELECT * except (payload) FROM `bigquery-public-data.samples.github_nested` LIMIT 1000

Example of select * except a especific field inside the nested column
SELECT * REPLACE (
  ARRAY(SELECT AS STRUCT * EXCEPT (old_mode) FROM UNNEST(difference)) AS difference
)
FROM `bigquery-public-data.github_repos.commits`
LIMIT 1000;

https://stackoverflow.com/questions/41019739/bigquery-select-except-nested-column

https://stackoverflow.com/questions/41021823/bigquery-select-except-two-columns

**Changing a nested field**

https://medium.com/firebase-developers/using-the-unnest-function-in-bigquery-to-analyze-event-parameters-in-analytics-fb828f890b42

Data STRUCT

nested_field.list.element.columns-with-data

STRUCT list
array[
STRUCT element
STRUCT <fields>
]

SELECT
ARRAY(SELECT AS STRUCT
        	field1,
        	field2,
        	CAST(null as String) as field3,
        	field_4 as field4
          FROM UNNEST
              ((select ARRAY(select nested.element as new_nested from `dataset.table`
                CROSS JOIN UNNEST (nested_field.list) as nested) as new_nested)))
  as proposedprices,
  cast(tenant as STRING) as tenant_id,
  _PARTITIONTIME as partition_date
