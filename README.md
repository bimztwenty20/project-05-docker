🐳 Dockerized ETL Pipeline

A containerized ETL pipeline built with Python, Pandas, PostgreSQL, and Docker Compose.

<p align="center">






</p>
📌 Overview

A small end-to-end ETL pipeline that reads customer and order data from CSV files, validates and transforms the data, separates invalid records, and loads clean data into PostgreSQL.

CSV → ETL → PostgreSQL

🏗️ Architecture
Clean
Invalid
customers.csv
orders.csv
ETL Container
Transform & Validate
("PostgreSQL")
Rejected CSV
customers
orders
🛠️ Tech Stack
Technology	Role
🐍 Python 3.12	ETL application
🐼 Pandas	Data processing
🐘 PostgreSQL 16	Database
🐳 Docker	Containerization
🔗 Docker Compose	Service orchestration
🔌 psycopg2	PostgreSQL connection
🔄 ETL Flow
Extract

Reads:

data/customers.csv
data/orders.csv

Transform & Validate

Customer total_belanja values are converted to numeric values.

Invalid values are separated from clean records.

Load

Clean customers → PostgreSQL customers

Orders → PostgreSQL orders

Invalid customers → customers_rejected.csv

Tables are created automatically when they do not exist.

📊 Results
Dataset	Input	Loaded	Rejected
Customers	8	7	1
Orders	4	4	0

The pipeline successfully processes the sample dataset while retaining invalid records separately.

🚀 Quick Start
1. Configure environment
cp .env.example .env

2. Start PostgreSQL
docker compose up -d postgres

3. Run ETL
docker compose run --rm etl


Expected output:

Starting ETL...
Tables ready
Loaded 8 rows
Orders rows: 4
Clean rows: 7
Rejected rows : 1
Environment: development
ETL Completed!

4. Verify
docker compose exec postgres \
  psql -U etl -d project05 \
  -c "SELECT COUNT(*) FROM customers;"

7

docker compose exec postgres \
  psql -U etl -d project05 \
  -c "SELECT COUNT(*) FROM orders;"

4

💾 Persistence

PostgreSQL data is stored in a named Docker volume:

postgres_data
    ↓
/var/lib/postgresql/data


This allows database records to persist across PostgreSQL container recreation.

📂 Project Structure
project-05-docker/
├── app/
│   └── main.py
├── data/
│   ├── customers.csv
│   └── orders.csv
├── .env.example
├── .gitignore
├── .dockerignore
├── compose.yaml
├── Dockerfile
├── README.md
└── requirements.txt

🎯 Key Features

🐍 Containerized Python ETL

🐼 Pandas data transformation

✅ Data validation

🚫 Rejected-record handling

🐘 PostgreSQL integration

❤️ PostgreSQL healthcheck

🔗 Docker Compose networking

💾 Persistent database volume

⚙️ Environment-based configuration

👨‍💻 Portfolio Project

A hands-on Data Engineering project demonstrating ETL development, containerization, database integration, and reproducible local data workflows.