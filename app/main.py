import pandas as pd
import os
import psycopg2

INPUT_FILE = "/app/data/customers.csv"
CLEAN_FILE = "/app/output/customers_clean.csv"
REJECTED_FILE = "/app/output/customers_rejected.csv"
ORDERS_FILE = "/app/data/orders.csv"


def get_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )
    
def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY,
            nama TEXT,
            umur INTEGER,
            kota TEXT,
            total_belanja NUMERIC,
            updated_at TIMESTAMP
        );
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            amount NUMERIC,
            updated_at TIMESTAMP
        );
        """
    )

    conn.commit()
    cur.close()
    conn.close()

    print("Tables ready")
    
def load_to_postgres(df):
    conn = get_connection()
    cur = conn.cursor()

    for _, row in df.iterrows():
        cur.execute(
            """
            INSERT INTO customers
                (id, nama, umur, kota, total_belanja, updated_at)
            VALUES
                (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (id)
            DO UPDATE SET
                nama = EXCLUDED.nama,
                umur = EXCLUDED.umur,
                kota = EXCLUDED.kota,
                total_belanja = EXCLUDED.total_belanja,
                updated_at = EXCLUDED.updated_at
            """,
            (
                row["id"],
                row["nama"],
                row["umur"],
                row["kota"],
                row["total_belanja"],
                row["updated_at"],
            ),
        )

    conn.commit()
    cur.close()
    conn.close()

def load_orders_to_postgres(df):
    conn = get_connection()
    cur = conn.cursor()

    for _, row in df.iterrows():
        cur.execute(
            """
            INSERT INTO orders
                (order_id, customer_id, amount, updated_at)
            VALUES
                (%s, %s, %s, %s)
            ON CONFLICT (order_id)
            DO UPDATE SET
                customer_id = EXCLUDED.customer_id,
                amount = EXCLUDED.amount,
                updated_at = EXCLUDED.updated_at
            """,
            (
                row["order_id"],
                row["customer_id"],
                row["amount"],
                row["updated_at"],
            ),
        )

    conn.commit()
    cur.close()
    conn.close()


def main():
    print("Starting ETL...")
    
    create_tables()
    
    #Extract
    df = pd.read_csv(INPUT_FILE)
    
    print(f"Loaded {len(df)} rows")
    
    #Transform
    df["total_belanja"] = pd.to_numeric(
        df["total_belanja"],
        errors="coerce"
    )
    
    #Validate
    rejected = df[df["total_belanja"].isna()].copy()
    clean = df[df["total_belanja"].notna()].copy()
    
    #load CSV
    clean.to_csv(CLEAN_FILE, index=False)
    rejected.to_csv(REJECTED_FILE, index=False)
    
    # Load customers
    load_to_postgres(clean)

    # Extract orders
    orders_df = pd.read_csv(ORDERS_FILE)

    # Transform orders
    orders_df["amount"] = pd.to_numeric(
        orders_df["amount"],
        errors="coerce"
    )

    # Load orders
    load_orders_to_postgres(orders_df)

    print(f"Orders rows: {len(orders_df)}")

    
    #Load PostgreSQL
    conn = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "postgres"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        dbname=os.getenv("POSTGRES_DB", "project05"),
        user=os.getenv("POSTGRES_USER", "etl"),
        password=os.getenv("POSTGRES_PASSWORD", "etlpassword"),
    )
    
    cur = conn.cursor()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS customers (
           id INTEGER PRIMARY KEY,
           nama TEXT,
           umur INTEGER,
           kota TEXT,
           total_belanja NUMERIC,
           updated_at TIMESTAMP
        )
        """
    )
    
    for _, row in clean.iterrows():
        cur.execute("""
            INSERT INTO customers
                (id, nama, umur, kota, total_belanja, updated_at)
            VALUES
                (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO UPDATE SET
                nama = excluded.nama,
                umur = excluded.umur,
                kota = excluded.kota,
                total_belanja = excluded.total_belanja,
                updated_at = excluded.updated_at
            """,
            (
                int(row["id"]),
                row["nama"],
                int(row["umur"]),
                row["kota"] if pd.notna(row["kota"]) else None,
                row["total_belanja"],
                row["updated_at"],
            ),
        )
        
    conn.commit()
    
    cur.close()
    conn.close()

    
    print(f"Clean rows: {len(clean)}")
    print(f"Rejected rows : {len(rejected)}")
    print(f"Environment: {os.getenv('APP_ENV')}")
    print("ETL Completed!")
    
    
if __name__ == "__main__":
    main()