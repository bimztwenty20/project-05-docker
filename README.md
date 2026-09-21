Dockerized ETL Pipeline with PostgreSQL

A containerized ETL pipeline built with Python, Pandas, Docker Compose, and PostgreSQL.

The project extracts customer and order data from CSV files, validates and transforms the data, separates invalid records, and loads clean records into PostgreSQL.

Architecture
                    ┌──────────────────┐
                    │   CSV Data       │
                    │                  │
                    │ customers.csv    │
                    │ orders.csv       │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │   ETL Container  │
                    │                  │
                    │ Python + Pandas  │
                    │ Validation       │
                    │ Transformation   │
                    └───────┬──────────┘
                            │
                  ┌─────────┴─────────┐
                  │                   │
                  ▼                   ▼
        ┌──────────────────┐   ┌──────────────────┐
        │ Rejected CSV     │   │   PostgreSQL     │
        │                  │   │                  │
        │ Invalid records  │   │ customers        │
        │                  │   │ orders           │
        └──────────────────┘   └──────────────────┘

Tech Stack

Python 3.12

Pandas

PostgreSQL 16

Docker

Docker Compose

psycopg2

ETL Flow
1. Extract

The pipeline reads:

data/customers.csv

data/orders.csv

2. Transform

Customer total_belanja values are converted to numeric values using Pandas.

Invalid numeric values are converted to NaN.

3. Validate

Customer records are separated into:

Clean records — valid total_belanja

Rejected records — missing or invalid total_belanja

4. Load

Clean customer records are loaded into the PostgreSQL customers table.

Order records are loaded into the PostgreSQL orders table.

The pipeline creates the required tables automatically using:

CREATE TABLE IF NOT EXISTS

Database Schema
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
Docker Architecture

The application consists of two services:

ETL

The ETL service runs the Python pipeline.

It mounts:

./data   → /app/data
./output → /app/output


This allows the container to read input files and write generated output files to the host.

PostgreSQL

PostgreSQL runs as a separate Compose service.

Database storage uses a named Docker volume:

postgres_data → /var/lib/postgresql/data


This keeps database data independent from the PostgreSQL container lifecycle.

Environment Configuration

Runtime configuration is provided through .env.

Example:

APP_ENV=development
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=project05
POSTGRES_USER=etl
POSTGRES_PASSWORD=etlpassword


The .env file is intentionally excluded from Git using .gitignore.

Running the Project
1. Start PostgreSQL
docker compose up -d postgres


Check the service:

docker compose ps


PostgreSQL should report:

Up (healthy)

2. Run the ETL
docker compose run --rm etl


Expected output:

Starting ETL...
Tables ready
Loaded 8 rows
Orders rows: 4
Clean rows: 7
Rejected rows: 1
Environment: development
ETL Completed!

Verify PostgreSQL

Check customers:

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

Data Quality Result

The sample input contains 8 customer records.

The pipeline produces:

8 input records
       │
       ├── 7 clean records
       │       └── loaded into PostgreSQL
       │
       └── 1 rejected record
               └── customers_rejected.csv


The rejected record is retained separately instead of silently being discarded.

Persistence Test

PostgreSQL uses a named Docker volume:

postgres_data


The project was tested by:

Loading 7 customers and 4 orders.

Stopping the PostgreSQL container.

Removing the container without removing the named volume.

Starting PostgreSQL again.

Verifying that the data remained available.

Result:

customers: 7
orders:    4


This confirms that database data persists independently of the PostgreSQL container.

Service Dependency

The ETL service depends on PostgreSQL health:

depends_on:
  postgres:
    condition: service_healthy


PostgreSQL uses pg_isready as its healthcheck.

This prevents the ETL container from attempting database operations before PostgreSQL is ready to accept connections.

Useful Commands

Validate Compose configuration:

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


Do not use docker compose down -v if you want to preserve the PostgreSQL named volume.

Project Goals

This project demonstrates practical experience with:

Containerizing Python applications

Building ETL pipelines

Data validation and rejected-record handling

PostgreSQL integration

Docker Compose service orchestration

Environment-based configuration

Docker bind mounts

Docker named volumes

Service healthchecks

Container-to-container networking

Persistent database storage

Reproducible local development environments
