import os
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

# 1. Load and prepare dataset
def load_and_prepare_data(file_path: str, n_rows: int = None) -> pd.DataFrame:
    df = pd.read_parquet(file_path)
    print("Dataset loaded. Preview:")
    print(df.head())

    if n_rows:
        df = df.head(n_rows)

    # Sanitize column names
    df.columns = [
        c.replace(" ", "_")
         .replace("(", "")
         .replace(")", "")
         .replace("-", "_")
         .replace("/", "_")
         .lower()
        for c in df.columns
    ]

    print("\nSanitized columns:")
    print(df.columns.tolist())
    return df

# 2. Map pandas dtypes to PostgreSQL types
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

def generate_columns_sql(df: pd.DataFrame, key_cols: list = None) -> str:
    cols_sql = []
    for col, dtype in df.dtypes.items():
        col_def = f"{col} {map_dtype_to_pg(dtype)}"
        cols_sql.append(col_def)
    
    key_sql = f", PRIMARY KEY ({', '.join(key_cols)})" if key_cols else ""
    return ", ".join(cols_sql) + key_sql

# 3. Create table and insert data into PostgreSQL
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
    ) as conn_pg:
        conn_pg.autocommit = True
        with conn_pg.cursor() as cur:

            # Drop table if exists
            cur.execute(f"DROP TABLE IF EXISTS {table_name};")
            print(f"Table '{table_name}' dropped if existed.")

            # Create table with composite primary key
            cols_sql = generate_columns_sql(df, key_cols=key_cols)
            cur.execute(f"CREATE TABLE {table_name} ({cols_sql});")
            if key_cols:
                print(f"Table '{table_name}' created with composite key {key_cols}.")
            else:
                print(f"Table '{table_name}' created without primary key.")

            # Convert pd.NA and NaN to None for PostgreSQL
            for col in df.columns:
                df[col] = df[col].apply(lambda x: None if pd.isna(x) else x)

            # Insert data
            records = [tuple(x) for x in df.to_numpy()]
            execute_values(
                cur,
                f"INSERT INTO {table_name} ({', '.join(df.columns)}) VALUES %s",
                records
            )
            print(f"{len(df)} rows inserted into '{table_name}'.")

# 4. Main function
def main():
    file_path = "data/gdsc_clean.parquet"
    table_name = "razzouk"
    n_rows = 100
    # Use sanitized lowercase column names for primary key
    key_cols = ["cosmic_id", "drug_id"]

    df_to_insert = load_and_prepare_data(file_path, n_rows)
    create_and_insert_table(df_to_insert, table_name, key_cols=key_cols)

if __name__ == "__main__":
    main()