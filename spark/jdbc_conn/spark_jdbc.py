from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName('spark_jdbc') \
    .getOrCreate()

user_pass = 'my_pass'
sql_statement = '(select top 10 * from mydb.tbl) AS query'
sql_df = spark.read \
    .format("jdbc") \
    .option("driver","com.microsoft.sqlserver.jdbc.SQLServerDriver") \
    .option("url", "jdbc:sqlserver://sql-server-address;DatabaseName=mydb") \
    .option("dbtable", sql_statement) \
    .option("user", "sqlserver_user") \
    .option("password", user_pass) \
    .load()

sql_df.show(truncate=False )
