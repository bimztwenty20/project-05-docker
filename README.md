🐳 Dockerized ETL Pipeline

A containerized ETL pipeline built with Python, Pandas, PostgreSQL, and Docker Compose.

<p align="center">






</p>
📌 Overview

This project implements a small end-to-end ETL pipeline that processes customer and order data from CSV files and loads clean records into PostgreSQL.

The pipeline demonstrates:

CSV data extraction

Data transformation with Pandas

Data validation

Rejected-record handling

PostgreSQL loading

Docker containerization

Docker Compose orchestration

Persistent database storage

Pipeline

CSV → Extract → Transform → Validate → PostgreSQL

Invalid customer records are separated into a rejected CSV instead of being silently discarded.

🏗️ Architecture
Clean customers
Invalid customers
customers.csv
orders.csv
ETL Container
Transform & Validate
("PostgreSQL")
Rejected CSV
customers
orders
🛠️ Tech Stack
Technology	Purpose
Python 3.12	ETL application
Pandas	Data processing & validation
PostgreSQL 16	Relational database
psycopg2	PostgreSQL connectivity
Docker	Application containerization
Docker Compose	Multi-container orchestration
🔄 ETL Process
1. Extract

The pipeline reads:

data/
├── customers.csv
└── orders.csv

2. Transform

Customer total_belanja values are converted to numeric values using Pandas.

Invalid numeric values are converted to NaN.

3. Validate

Customer records are separated into:

Record Type	Description
✅ Clean	Valid total_belanja
❌ Rejected	Missing or invalid total_belanja
4. Load

Clean customer records are loaded into the customers table.

Order records are loaded into the orders table.

The required tables are created automatically using:

CREATE TABLE IF NOT EXISTS

📊 Data Quality Result

The sample dataset contains 8 customer records.

Metric	Result
Input customers	8
Clean customers	7
Rejected customers	1
Orders loaded	4

The rejected record is retained separately in:

output/customers_rejected.csv


This prevents invalid data from being silently lost.

🗄️ Database Schema
customers
Column	Type	Description
id	INTEGER	Customer identifier
nama	TEXT	Customer name
umur	INTEGER	Customer age
kota	TEXT	Customer city
total_belanja	NUMERIC	Total customer spending
updated_at	TIMESTAMP	Last update timestamp
orders
Column	Type	Description
order_id	INTEGER	Order identifier
customer_id	INTEGER	Customer identifier
amount	NUMERIC	Order amount
updated_at	TIMESTAMP	Last update timestamp
🐳 Docker Architecture

The application consists of two services:

ETL

The ETL container runs the Python pipeline.

Host directories are mounted into the container:

./data   → /app/data
./output → /app/output


This allows the container to read input files and write generated output files.

PostgreSQL

PostgreSQL runs as a separate Docker Compose service.

Database storage uses a named volume:

postgres_data
      ↓
/var/lib/postgresql/data


This keeps database data independent from the PostgreSQL container lifecycle.

❤️ Service Dependency

The ETL service waits for PostgreSQL to become healthy before starting.

depends_on:
  postgres:
    condition: service_healthy


PostgreSQL uses pg_isready as its healthcheck:

healthcheck:
  test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]


This prevents the ETL process from attempting database operations before PostgreSQL is ready.

⚙️ Environment Configuration

Runtime configuration is provided through environment variables.

Create .env from the example:

cp .env.example .env


Example configuration:

APP_ENV=development

POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=project05
POSTGRES_USER=etl
POSTGRES_PASSWORD=etlpassword


.env is excluded from Git because it contains environment-specific configuration and credentials.

🚀 Running the Project
1. Start PostgreSQL
docker compose up -d postgres


Check the service:

docker compose ps


PostgreSQL should show:

Up (healthy)

2. Run the ETL pipeline
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

🔍 Verify the Database

Check customer records:

docker compose exec postgres \
  psql -U etl -d project05 \
  -c "SELECT COUNT(*) FROM customers;"


Expected:

7


Check orders:

docker compose exec postgres \
  psql -U etl -d project05 \
  -c "SELECT COUNT(*) FROM orders;"


Expected:

4


View customer data:

docker compose exec postgres \
  psql -U etl -d project05 \
  -c "SELECT id, nama, total_belanja FROM customers ORDER BY id;"

💾 Database Persistence

PostgreSQL uses the named Docker volume:

postgres_data


The database was tested by:

Loading customer and order data.

Stopping the PostgreSQL container.

Removing/recreating the PostgreSQL container.

Starting PostgreSQL again.

Verifying the records remained available.

Result:

customers: 7
orders:    4


This demonstrates persistent database storage across container recreation.

Do not use docker compose down -v if you want to preserve the PostgreSQL volume.

📂 Project Structure
project-05-docker/
│
├── app/
│   └── main.py
│
├── data/
│   ├── customers.csv
│   └── orders.csv
│
├── output/
│   └── customers_rejected.csv
│
├── .dockerignore
├── .env.example
├── .gitignore
├── compose.yaml
├── Dockerfile
├── README.md
└── requirements.txt

🧪 Useful Commands

Validate Docker Compose configuration:

docker compose config


Build the ETL image:

docker compose build


Run the ETL:

docker compose run --rm etl


View services:

docker compose ps


View PostgreSQL logs:

docker compose logs postgres


Open PostgreSQL shell:

docker compose exec postgres \
  psql -U etl -d project05


Stop services:

docker compose down

🎯 Project Highlights

This project demonstrates practical experience with:

🐍 Python ETL development

🐼 Pandas data processing

🐘 PostgreSQL integration

🐳 Docker containerization

🔗 Docker Compose orchestration

✅ Data validation

🚫 Rejected-record handling

❤️ PostgreSQL healthchecks

🌐 Container-to-container networking

💾 Persistent Docker volumes

⚙️ Environment-based configuration

🔁 Reproducible local development

📌 Project Result

The pipeline successfully processes customer and order data in a containerized environment:

customers.csv ──┐
                ├──> ETL ──> PostgreSQL
orders.csv ─────┘       │
                        └──> Rejected CSV


8 customer records → 7 clean + 1 rejected

4 orders → 4 loaded

👨‍💻 Portfolio Project

Built as a hands-on Data Engineering project focused on ETL, Docker, PostgreSQL, and reproducible data workflows.