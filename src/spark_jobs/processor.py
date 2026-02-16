from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType

db_user = os.getenv("POSTGRES_USER", "alex")
db_password = os.getenv("POSTGRES_PASSWORD", "1111")
db_name = os.getenv("POSTGRES_DB", "fraud_detection")

spark = SparkSession.builder \
   .appName("FraudStreamingProcessor") \
   .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.3.4") \
   .config("spark.hadoop.fs.s3a.endpoint", "http://fraud_localstack:4566") \
   .config("spark.hadoop.fs.s3a.access.key", "test") \
   .config("spark.hadoop.fs.s3a.secret.key", "test") \
   .config("spark.hadoop.fs.s3a.path.style.access", "true") \
   .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
   .getOrCreate()

schema = StructType ([
   StructField("user_id", IntegerType(), True),
   StructField("amount", DoubleType(), True),
   StructField("timestamp", StringType(), True),
   StructField("location", StringType(), True)
])