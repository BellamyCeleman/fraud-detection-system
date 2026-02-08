import boto3
import json
import time
from typing import Dict, List, Optional


class TransactionDataLayer:
   def __init__(self,
                host: str = "localhost",
                port: int = 5432,
                dbname: str = "fraud_detection",
                user: str = "alex",
                password: str = "1111"):
      self.connection_params = {
         "host": host,
         "port": port,
         "dbname": dbname,
         "user": user,
         "password": password
      }
      self.s3 = boto3.client(
         "s3",
         endpoint_url="http://localhost:4566",
         aws_access_key_id="test",
         aws_secret_access_key="test",
         region_name="us-east-1"
      )
      self.bucket_name = "raw-transactions"
   
   def save_to_s3_batch(self, transactions: list):
      file_name = f"batch_{int(time.time() * 1000)}.json"
      body = json.dumps(transactions)

      self.s3.put_object(
         
      )




if __name__ == "__main__":
   data_layer = TransactionDataLayer()

   sample_transaction = {
      "transaction_id": "TXN-TEST-001",
      "user_id": 1,
      "amount": 150.50,
      "location": "New York",
      "timestamp": datetime.now(timezone.utc).isoformat(),
      "is_anomaly": False
   }

   data_layer.save_transaction(sample_transaction)
   print("Sample transaction saved")

