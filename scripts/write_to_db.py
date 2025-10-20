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

        # Step 2: Load dataset
        df = pd.read_csv("data/gdsc_clean.csv")
        print("Dataset preview:")
        print(df.head())

        # Step 3: Prepare table name and data
        table_name = "razzouk"
        df_to_insert = df.head(100)

        # Step 4: Sanitize column names for PostgreSQL
        df_to_insert.columns = [c.replace(" ", "_").replace("(", "").replace(")", "").replace("-", "_") for c in df_to_insert.columns]

        # Step 5: Create table
        cols_sql = ", ".join(f"{col} TEXT" for col in df_to_insert.columns)
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