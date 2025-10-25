import os
import pandas as pd
import psycopg2

# Step 0: Read PostgreSQL credentials from environment variables
PG_HOST = os.environ["PG_HOST"]
PG_PORT = os.environ["PG_PORT"]
PG_USER = os.environ["PG_USER"]
PG_PASS = os.environ["PG_PASS"]

print("PostgreSQL credentials loaded from environment variables.")

# Step 1: Connect to PostgreSQL
with psycopg2.connect(
    host=PG_HOST,
    port=PG_PORT,
    user=PG_USER,
    password=PG_PASS,
    database="homeworks"
) as conn_pg:
    with conn_pg.cursor() as cur:

        print("Connected to PostgreSQL successfully!")

        # Step 2: Load dataset from Parquet
        df = pd.read_parquet("data/gdsc_clean.parquet")
        print("Dataset preview:")
        print(df.head())

        # Step 3: Prepare table name and subset
        table_name = "razzouk"
        df_to_insert = df.head(100)

        # Step 4: Sanitize column names
        df_to_insert.columns = [
            c.replace(" ", "_").replace("(", "").replace(")", "").replace("-", "_")
            for c in df_to_insert.columns
        ]

        # Step 5: Map pandas dtypes to PostgreSQL types
        dtype_map = {
            "int64": "BIGINT",
            "float64": "DOUBLE PRECISION",
            "bool": "BOOLEAN",
            "category": "TEXT",
            "string": "TEXT",
            "object": "TEXT"
        }

        cols_sql = ", ".join(
            f"{col} {dtype_map.get(str(dtype), 'TEXT')}"
            for col, dtype in df_to_insert.dtypes.items()
        )

        create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({cols_sql});"
        cur.execute(create_table_sql)
        print(f"Table '{table_name}' created (if it didn’t exist).")

        # Step 6: Insert rows into PostgreSQL
        for _, row in df_to_insert.iterrows():
            values = tuple(row)
            placeholders = ", ".join(["%s"] * len(values))
            insert_sql = f"INSERT INTO {table_name} VALUES ({placeholders})"
            cur.execute(insert_sql, values)

        print(f"{len(df_to_insert)} rows inserted into '{table_name}'.")

print("PostgreSQL connection closed automatically.")