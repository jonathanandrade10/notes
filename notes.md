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
