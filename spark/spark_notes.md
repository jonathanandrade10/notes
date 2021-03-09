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
