#!/usr/bin/env python3

import json
import random
from datetime import datetime
import time


class TransactionGenerator:
   LOCATIONS = [
      "New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
      "London", "Paris", "Berlin", "Tokyo", "Singapore"
   ]

   USERS = [
      {"id": 1, "name": "Alice Johnson", "average_spending": 150.00},
      {"id": 2, "name": "Bob Smith", "average_spending": 320.00},
      {"id": 3, "name": "Carol White", "average_spending": 75.50},
      {"id": 4, "name": "David Brown", "average_spending": 450.00},
      {"id": 5, "name": "Emma Davis", "average_spending": 200.00},
   ]

   def __init__(self, anomaly_probability=0.05):
      self.anomaly_probability = anomaly_probability
      self.transaction_count = 0

   def generate_normal_transaction(self, user):
      avg = user["average_spending"]
      amount = round(random.uniform(avg * 0.6, avg * 1.4), 2)
      location = random.choice(self.LOCATIONS[:5])

      return {
         "transaction_id": f"TXN-{int(time.time() * 1000)}-{random.randint(1000, 9999)}",
         "user_id": user["id"],
         "amount": amount,
         "location": location,
         "timestamp": datetime.utcnow().isoformat() + "Z",
         "is_anomaly": False
      }

   def generate_anomalous_transaction(self, user):
      avg = user["average_spending"]
      anomaly_type = random.choice(["high_amount", "extreme_amount", "unusual_location"])

      if anomaly_type == "high_amount":
         amount = round(avg * random.uniform(3.0, 5.0), 2)
         location = random.choice(self.LOCATIONS[:5])

      elif anomaly_type == "extreme_amount":
         amount = round(avg * random.uniform(6.0, 10.0), 2)
         location = random.choice(self.LOCATIONS)

      else:
         amount = round(avg * random.uniform(0.8, 1.5), 2)
         location = random.choice(self.LOCATIONS[5:])

      return {
         "transaction_id": f"TXN-{int(time.time() * 1000)}-{random.randint(1000, 9999)}",
         "user_id": user["id"],
         "amount": amount,
         "location": location,
         "timestamp": datetime.utcnow().isoformat() + "Z",
         "is_anomaly": True
      }

   def generate_transaction(self):
      user = random.choice(self.USERS)

      if random.random() < self.anomaly_probability:
         transaction = self.generate_anomalous_transaction(user)
      else:
         transaction = self.generate_normal_transaction(user)

      self.transaction_count += 1
      return transaction


def main():
   generator = TransactionGenerator(anomaly_probability=0.05)

   try:
      while True:
         transaction = generator.generate_transaction()
         print(json.dumps(transaction, indent=2))
         print("-" * 80)
         time.sleep(1)

   except KeyboardInterrupt:
      pass


if __name__ == "__main__":
   main()