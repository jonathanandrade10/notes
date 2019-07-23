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

## Big Query

Strongly avoid run functions or parse in a partition_date field, it may cause a Full Scan on the table.

select * from dataset.table t
where format_date('%Y%m%d', t.partition_date) = '20190618' --- 4.6TB


Change the function or parse to the value not on the partition field. 

select * from dataset.table t
where t.partition_date = PARSE_DATE('%Y%m%d', '20190618') ---87GB


Loop replicating data to other range of data
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
