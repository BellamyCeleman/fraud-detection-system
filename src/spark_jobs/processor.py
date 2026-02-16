import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when
from pyspark.sql.types import StructType, StructField, IntegerType, DoubleType, StringType

def create_spark_session():
    return SparkSession.builder \
        .appName("FraudProcessor") \
        .config("spark.jars.packages", "org.postgresql:postgresql:42.7.1,org.apache.hadoop:hadoop-aws:3.3.4") \
        .config("spark.hadoop.fs.s3a.endpoint", os.getenv("S3_ENDPOINT", "http://localstack:4566")) \
        .config("spark.hadoop.fs.s3a.access.key", os.getenv("AWS_ACCESS_KEY_ID", "test")) \
        .config("spark.hadoop.fs.s3a.secret.key", os.getenv("AWS_SECRET_ACCESS_KEY", "test")) \
        .config("spark.hadoop.fs.s3a.path.style.access", "true") \
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
        .getOrCreate()

def main():
   spark = create_spark_session()

   schema = StructType ([
      StructField("user_id", IntegerType(), True),
      StructField("amount", DoubleType(), True),
      StructField("timestamp", StringType(), True),
      StructField("location", StringType(), True)
   ])

   df_transactions = spark.read.schema(schema).json("s3a://raw-transactions/*/*.json")

   db_url = "jdbc:" + os.getenv("DATABASE_URL", "postgresql://postgres:5432/fraud_detection")
   db_user = os.getenv("POSTGRES_USER", "alex")
   db_password = os.getenv("POSTGRES_PASSWORD", "1111")

   df_users = spark.read \
      .format("jdbc") \
      .option("url", db_url) \
      .option("dbtable", "users") \
      .option("user", db_user) \
      .option("password", db_password) \
      .option("driver", "org.postgresql.Driver") \
      .load()
   
   enriched_df = df_transactions.join(df_users, df_transactions.user_id == df_users.id) \
        .withColumn("is_suspicious", col("amount") > (col("avg_spending") * 3))
   
   enriched_df.write \
        .mode("overwrite") \
        .parquet("s3a://processed-transactions/daily_batch/")

   spark.stop()

if __name__ == "__main__":
    main()