import os
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

def load_and_prepare_data(parquet_path: str, n_rows: int = None) -> pd.DataFrame:
    df = pd.read_parquet(parquet_path)
    if n_rows:
        df = df.head(n_rows)
    
    # Sanitize columns: lowercase and replace spaces/special chars
    df.columns = [
        c.replace(" ", "_")
         .replace("(", "")
         .replace(")", "")
         .replace("-", "_")
         .replace("/", "_")
         .lower()
        for c in df.columns
    ]
    return df

def map_dtype_to_pg(dtype):
    dtype_name = str(dtype)
    if dtype_name in ["Int64", "int64", "Int32", "int32", "Int16", "int16"]:
        return "BIGINT"
    elif dtype_name in ["float64", "Float64", "float32"]:
        return "DOUBLE PRECISION"
    elif "bool" in dtype_name.lower():
        return "BOOLEAN"
    else:
        return "TEXT"

def generate_columns_sql(df: pd.DataFrame, key_cols: list = None) -> str:
    cols_sql = [f"{col} {map_dtype_to_pg(dtype)}" for col, dtype in df.dtypes.items()]
    key_sql = f", PRIMARY KEY ({', '.join(key_cols)})" if key_cols else ""
    return ", ".join(cols_sql) + key_sql

def create_and_insert_table(df: pd.DataFrame, table_name: str, key_cols: list = None):
    PG_HOST = os.environ["PG_HOST"]
    PG_PORT = os.environ["PG_PORT"]
    PG_USER = os.environ["PG_USER"]
    PG_PASS = os.environ["PG_PASS"]

    with psycopg2.connect(
        host=PG_HOST,
        port=PG_PORT,
        user=PG_USER,
        password=PG_PASS,
        database="homeworks"
    ) as conn:
        conn.autocommit = True
        with conn.cursor() as cur:
            # Drop and create table
            cur.execute(f"DROP TABLE IF EXISTS {table_name};")
            cols_sql = generate_columns_sql(df, key_cols)
            cur.execute(f"CREATE TABLE {table_name} ({cols_sql});")
            
            # Replace NaNs/None for insertion
            df_clean = df.applymap(lambda x: None if pd.isna(x) else x)
            records = [tuple(x) for x in df_clean.to_numpy()]
            
            execute_values(
                cur,
                f"INSERT INTO {table_name} ({', '.join(df.columns)}) VALUES %s",
                records
            )
            print(f"{len(df)} rows inserted into '{table_name}'.")

def main(parquet_path, table_name, n_rows, key_cols):
    # Load and prepare data
    df_to_insert = load_and_prepare_data(parquet_path, n_rows)

    # Create table and insert into PostgreSQL
    create_and_insert_table(df_to_insert, table_name, key_cols=key_cols)