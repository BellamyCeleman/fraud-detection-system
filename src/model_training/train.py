import numpy as np
import pandas as pd
import os
import torch
import torch.nn as nn
import torch.optim as optim
from io import BytesIO
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import boto3

from config import TRAIN_CONFIG

from dotenv import load_dotenv

load_dotenv("dev.env")

class Autoencoder(nn.Module):
   def __init__(self, input_dim):
      super(Autoencoder, self).__init__()
      self.encoder = nn.Sequential(
         nn.Linear(input_dim, 16),
         nn.ReLU(),
         nn.Linear(16, 8),
         nn.ReLU(),
         nn.Linear(8, 4),
      )
      self.decoder = nn.Sequential(
         nn.Linear(4, 8),
         nn.ReLU(),
         nn.Linear(8, 16),
         nn.ReLU(),
         nn.Linear(16, input_dim),
      )
   def forward(self, x):
      x = self.encoder(x)
      x = self.decoder(x)
      return x

def load_data_from_s3():
   s3 = boto3.client(
      's3',
      endpoint_url=os.getenv("S3_ENDPOINT", "http://localstack:4566"),
      aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "test"),
      aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "test")
   )
   
   bucket = "processed-transactions"

   try:
      s3.head_bucket(Bucket=bucket)
   except:
      # Creating if didnt exist
      print("Exception: Initialization \"processed-transactions\" bucket")
      s3.create_bucket(Bucket=bucket)

   response = s3.list_objects_v2(Bucket=bucket, Prefix="daily_batch/")
    
   all_df = []
   for obj in response.get('Contents', []):
      if obj['Key'].endswith('.parquet'):
         file_obj = s3.get_object(Bucket=bucket, Key=obj['Key'])
         all_df.append(pd.read_parquet(BytesIO(file_obj['Body'].read())))
   
   if not all_df:
      return pd.DataFrame()

   return pd.concat(all_df, ignore_index=True)

def train():
   df = load_data_from_s3()

   features = ['amount', 'avg_spending', 'user_id'] 
   data = df[features].values.astype(np.float32)

   scaler = StandardScaler()
   data_scaled = scaler.fit_transform(data)
   
   X_train, X_test = train_test_split(
      data_scaled, 
      test_size=TRAIN_CONFIG["test_size"], 
      random_state=TRAIN_CONFIG["random_state"]
   )
   X_train_tensor = torch.FloatTensor(X_train)
   
   model = Autoencoder(input_dim=len(features))
   criterion = nn.MSELoss()
   optimizer = optim.Adam(model.parameters(), lr=TRAIN_CONFIG["lr"])

   for epoch in range(TRAIN_CONFIG["epochs"]):
      model.train()
      optimizer.zero_grad()
      output = model(X_train)
      loss = criterion(output, X_train)
      loss.backward()
      optimizer.step()
   
   dummy_input = torch.randn(1, len(features))

   torch.onnx.export(model, dummy_input, "onnx_path")

if __name__ == "__main__":
   train()
   # print(os.getenv("S3_ENDPOINT", "http://localstack:4566"))