import os
import json
import time
import random
import uuid
from datetime import datetime

import boto3
from sqlalchemy.orm import Session
from database import SessionLocal
from app_api.models import User

class TransactionGenerator:
   def __init__(self):
      # 1. Load configuration
      self.s3_endpoint = os.getenv("S3_ENDPOINT", "http://localstack:4566")
      self.bucket_name = "raw-transactions"

      # 2. Setup S3 Client once
      self.s3 = boto3.client(
         "s3",
         endpoint_url=self.s3_endpoint,
         aws_access_key_id="test",
         aws_secret_access_key="test",
         region_name="us-east-1"
      )

      # 3. DB Session placeholder
      self.db: Session = SessionLocal()

   def setup_infrastructure(self):
      """Pre-flight checks: create bucket if missing."""
      try:
         self.s3.create_bucket(Bucket=self.bucket_name)
         print(f"[*] S3 Bucket '{self.bucket_name}' ready.")
      except Exception as e:
         print(f"[!] S3 Setup failed: {e}")

   def _get_active_users(self):
      """Fetch IDs of users available in Postgres."""
      return [u.id for u in self.db.query(User.id).all()]

   def create_payload(self, user_id: int):
      """Build the transaction dictionary."""
      return {
         "transaction_id": str(uuid.uuid4()),
         "user_id": user_id,
         "amount": round(random.uniform(5.0, 1500.0), 2),
         "timestamp": datetime.utcnow().isoformat(),
         "location": random.choice(["New York", "London", "Berlin", "Tokyo"])
      }

   def stream(self, interval: int = 1):
      """Main loop to produce and upload data."""
      self.setup_infrastructure()
      user_ids = self._get_active_users()

      if not user_ids:
         print("[!] No users found. Exit.")
         return

      print(f"[*] Streaming for {len(user_ids)} users...")
      try:
         while True:
               user_id = random.choice(user_ids)
               data = self.create_payload(user_id)

               # Upload to S3
               key = f"inbox/{user_id}/{data['transaction_id']}.json"
               self.s3.put_object(
                  Bucket=self.bucket_name,
                  Key=key,
                  Body=json.dumps(data)
               )

               print(f"[+] TX Uploaded: {data['transaction_id']}")
               time.sleep(interval)
      except KeyboardInterrupt:
         print("Stopping...")
      finally:
         self.db.close()

if __name__ == "__main__":
   # The entry point is now ultra-clean
   generator = TransactionGenerator()
   generator.stream(interval=1)