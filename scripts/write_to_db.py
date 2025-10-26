import os
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

# === 0. Read PostgreSQL credentials from environment variables ===
PG_HOST = os.environ["PG_HOST"]
PG_PORT = os.environ["PG_PORT"]
PG_USER = os.environ["PG_USER"]
PG_PASS = os.environ["PG_PASS"]

print("PostgreSQL credentials loaded from environment variables.")

# === 1. Connect to PostgreSQL ===
with psycopg2.connect(
    host=PG_HOST,
    port=PG_PORT,
    user=PG_USER,
    password=PG_PASS,
    database="homeworks"
) as conn_pg:
    conn_pg.autocommit = True
    with conn_pg.cursor() as cur:

        print("Connected to PostgreSQL successfully!")

        # === 2. Load dataset from Parquet ===
        df = pd.read_parquet("data/gdsc_clean.parquet")
        print("Dataset preview:")
        print(df.head())

        # === 3. Prepare table name and subset ===
        table_name = "razzouk"
        df_to_insert = df.head(100).copy()

        # === 4. Sanitize column names BEFORE creating table ===
        df_to_insert.columns = [
            c.replace(" ", "_")
             .replace("(", "")
             .replace(")", "")
             .replace("-", "_")
             .replace("/", "_")
             .lower()
            for c in df_to_insert.columns
        ]

        # === 5. Inspect data types ===
        print("\nDetected pandas dtypes:")
        print(df_to_insert.dtypes)

        # === 6. Map pandas dtypes to PostgreSQL types robustly ===
        def map_dtype_to_pg(dtype):
            dtype_name = str(dtype)
            if dtype_name in ["Int64", "int64", "Int32", "int32", "Int16", "int16"]:
                return "BIGINT"
            elif dtype_name in ["float64", "Float64", "float32"]:
                return "DOUBLE PRECISION"
            elif "bool" in dtype_name.lower():
                return "BOOLEAN"
            elif "category" in dtype_name.lower():
                return "TEXT"
            elif "string" in dtype_name.lower() or "object" in dtype_name.lower():
                return "TEXT"
            else:
                return "TEXT"

        cols_sql = ", ".join(
            f"{col} {map_dtype_to_pg(dtype)}"
            for col, dtype in df_to_insert.dtypes.items()
        )

        # === 7. Drop old table (if exists) and create new one ===
        cur.execute(f"DROP TABLE IF EXISTS {table_name};")
        print(f"Table '{table_name}' dropped if it existed.")

        create_table_sql = f"CREATE TABLE {table_name} ({cols_sql});"
        cur.execute(create_table_sql)
        print(f"Table '{table_name}' created with sanitized columns and correct types.")

        # === 8. Insert data efficiently using execute_values ===
        records = [tuple(x) for x in df_to_insert.to_numpy()]

        execute_values(
            cur,
            f"INSERT INTO {table_name} ({', '.join(df_to_insert.columns)}) VALUES %s",
            records
        )

        print(f"{len(df_to_insert)} rows inserted into '{table_name}'.")

print("PostgreSQL connection closed automatically.")