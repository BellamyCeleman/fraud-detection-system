# Real-time Fraud Detection System at Scale

A distributed end-to-end data engineering and machine learning pipeline designed to detect anomalous financial transactions. The system leverages **Apache Spark** for data enrichment, **PyTorch** for anomaly detection, and is orchestrated via **Docker** (with future migration to **Kubernetes**).



## 🏗 System Architecture

The project is divided into four main layers:
1. **Data Generation:** A Python-based generator mimicking real-time transaction streams, uploading JSON payloads to **AWS S3 (LocalStack)**.
2. **Storage Layer:** * **PostgreSQL:** Stores persistent user profiles and historical spending habits.
    * **LocalStack (S3):** Acts as the landing zone for raw transaction data.
3. **Processing Layer (Spark):** A **PySpark** ETL pipeline that joins real-time S3 data with Postgres metadata to engineer features.
4. **Inference Layer:** A **PyTorch** Autoencoder model that identifies fraud based on reconstruction error (Anomaly Detection).

---

## 🛠 Tech Stack

* **Languages:** Python (PySpark, PyTorch, FastAPI), SQL, Scala (Spark Core).
* **Infrastructure:** Docker & Docker Compose, LocalStack (AWS Simulation).
* **Big Data:** Apache Spark (Standalone Cluster).
* **Database:** PostgreSQL.
* **DevOps:** Environment variable management via `.env`, multi-container networking.

---

## 🚀 Getting Started

### 1. Prerequisites
* Docker and Docker Compose installed.
* Python 3.10+ (for local development).

### 2. Environment Setup
Clone the repository and create your local environment file:
```bash
cp .env.example dev.env
# Edit dev.env with your local credentials (POSTGRES_PASSWORD, etc.)