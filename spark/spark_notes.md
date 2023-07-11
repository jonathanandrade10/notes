## PySpark

A way of setting the python3 system path to look for PySpark module.

```
import os, sys
file_path = '/opt/cloudera/parcels/SPARK2/lib/spark2/python/'

sys.path.append(os.path.dirname(file_path))
sys.path.append(os.path.dirname('/opt/cloudera/parcels/SPARK2/lib/spark2/python/lib/')) sys.path.append(os.path.dirname('/opt/cloudera/parcels/SPARK2/lib/spark2/python/lib/py4j-0.10.7-src.zip/'))


import pyspark 
from pyspark.sql.session import SparkSession
```

**Kerberos call**
```
import os
current_username = os.environ['USER']
keytab_name = "/home/" + current_username + "/" + current_username + ".keytab"
kerberos_call = "kinit -kt " + keytab_name + " " + current_username
os.system(kerberos_call)
```

**Setting hadoop conf files**
```
os.environ['HADOOP_CONF_DIR'] = "/opt/cloudera/parcels/SPARK2/lib/spark2/conf/yarn-conf:/etc/hive/conf"
os.environ['YARN_CONF_DIR'] = "/etc/hadoop/conf.cloudera.yarn"
```

**Spark client local and job running on cluster**
```
os.environ['HADOOP_CONF_DIR'] = "/opt/cloudera/parcels/SPARK2/lib/spark2/conf/yarn-conf:/etc/hive/conf"
os.environ['YARN_CONF_DIR'] = "/etc/hadoop/conf.cloudera.yarn"
spark = SparkSession \
    .builder \
    .appName("Pyspark_app_name") \
    .master("yarn") \
    .getOrCreate()
```

**Databricks spark-xml**


Databricks jar


https://mvnrepository.com/artifact/com.databricks/spark-xml_2.12/0.5.0


```
df = spark.read.format("xml").options(rowTag="record").load("/home/folder/test.xml")
df.show()
```

spark submit with databricks jar that will be used by the pyspark job


```
./bin/spark-submit --jars ~/Downloads/spark-xml_2.12-0.5.0.jar ~/path_to_pyspark/pyspark_df_to_xml.py
```

## Spark Scala

**Merge Schema - empty parquet file with schema**

```
//creating a DataFrame of the data to be merged
val df = spark.read.option("mergeSchema", "true").parquet("/path_parquet/")

//get schema from DataFrame as StructType object
val schema = df.schema

//generating Empty DF from the schema merged=true
val emptyDF = spark.createDataFrame(sc.emptyRDD[Row], schema)

//Writing as a parquet file empty 
val path = "/test_mergeschema/"
emptyDF.repartition(1).write.mode(SaveMode.Overwrite).parquet(path)
```

**Reduce logs - Log level error**
```
import org.apache.log4j.{Level, Logger}

Logger.getLogger("org").setLevel(Level.ERROR)
```

**Drop Hive Partitions**

The example below shows how to drop hive partitions, an external table was used in this example and it raised an error if purge=true, spark wasn't able to drop partitions and delete it's content (probably purge wasn't available on that Hive version ?). Example ran on Spark 2.3.0, it needs to be configured as purge=false and the table needs invalidate metadata to refresh its partitions.

https://stackoverflow.com/a/63511779

```
//Seq[Map[String,String]]
val partitions = catalog.listPartitions("my_database", "my_table").map(_.spec)

filteredPartitions = Seq(Map("source" -> source, "hash" -> hash, "date" -> date))

// If you purge data, it gets deleted immediately and isn't moved to trash.
// This takes precedence over retainData, so even if you retainData but purge,
// your data is gone.

catalog.dropPartitions("my_database", "my_table", filteredPartitions,
          ignoreIfNotExists = true, purge = false, retainData = true)

```

**List S3 files**

```
val s3Path = "s3a://my.bucket/folder"

spark.conf.set("fs.s3a.access.key", "my_access_key")
spark.conf.set("fs.s3a.secret.key", "my_secret_key")
spark.conf.set("fs.s3a.endpoint", "s3.amazonaws.com")

//support for bucket with dots
spark.conf.set("fs.s3a.path.style.access", "true")



import org.apache.hadoop.fs.{FileSystem, Path}
import org.apache.hadoop.conf.Configuration
import java.net.URI


val fileSystem = FileSystem.get(URI.create(s3Path), new Configuration())
val it = fileSystem.listFiles(new Path(s3Path), true)

while (it.hasNext()) {  println(it.next().getPath.toUri.getPath) }
```

**Get dataframe differences**
```
//Return a new DataFrame containing rows in this DataFrame but not in another DataFrame while preserving duplicates.
df.exceptAll(df_prod).show()
```

**Read data from S3 - Jceks credentials**
```
val s3JceksFullPath =  "jceks://hdfs/my_folder/my_jceks_key_value.jceks"

val hadoopConf = spark.sparkContext.hadoopConfiguration
hadoopConf.set("hadoop.security.credential.provider.path", s"$s3JceksFullPath")
hadoopConf.set("spark.hadoop.hadoop.security.credential.provider.path", s"$s3JceksFullPath")

val bucket = "s3a://my-s3-bucket"
val path = "/my-data"

val df = spark.read.option("mergeSchema", "true").parquet(bucket + path)
```

**Libs for Spark S3**
aws-java-sdk-1.11.271.jar
aws-java-sdk-core-1.11.271.jar
aws-java-sdk-dynamodb-1.11.171.jar
aws-java-sdk-s3-1.11.171.jar
hadoop-aws-3.1.1.jar

## Spark Shell

**Spark Shell issue on MACM1**

```
Caused by: org.xerial.snappy.SnappyError: [FAILED_TO_LOAD_NATIVE_LIBRARY] no native library is found for os.name=Mac and os.arch=aarch64
```
https://stackoverflow.com/questions/71707903/org-xerial-snappy-snappyerror-failed-to-load-native-library-no-native-library

Download newer version (1.1.8.4 or higher seems to resolve) of snappy-java and replace it with the same older jar on the folder $SPARK_HOME/jars 
https://mvnrepository.com/artifact/org.xerial.snappy/snappy-java/1.1.8.4


**NoClassDefFoundError**

```
Error: A JNI error has occurred, please check your installation and try again
Exception in thread "main" java.lang.NoClassDefFoundError: org/slf4j/Logger
```
https://stackoverflow.com/questions/51531186/not-able-to-launch-spark-shell

add following entry in the spark-env.sh or on ~/.zshrc

```
export SPARK_DIST_CLASSPATH=$(hadoop classpath)
```


