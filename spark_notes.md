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
