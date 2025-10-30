import argparse
from etl import extract, transform, validate, load
import os

def main():
    parser = argparse.ArgumentParser(description="ETL pipeline for GDSC dataset")
    parser.add_argument(
        "--mode",
        type=str,
        choices=["extract", "transform", "validate", "load", "all"],
        required=True,
        help="Step of ETL to run: extract, transform, validate, load, or all"
    )
    args = parser.parse_args()

    file_id = os.getenv("GDSC_FILE_ID")
    raw_path = os.getenv("RAW_DATA_PATH", "data/raw/gdsc_raw.csv")
    parquet_path = os.getenv("PROCESSED_DATA_PATH", "data/processed/gdsc_clean.parquet")
    table_name = os.getenv("PG_TABLE_NAME", "razzouk")
    n_rows = int(os.getenv("N_ROWS", "100"))
    key_cols = os.getenv("KEY_COLS", "cosmic_id,drug_id").split(",") 

    if args.mode == "extract":
        extract.main(file_id, raw_path)
    elif args.mode == "transform":
        transform.main()
    elif args.mode == "validate":
        validate.main()
    elif args.mode == "load":
        load.main(parquet_path, table_name, n_rows, key_cols)
    elif args.mode == "all":
        extract.main(file_id, raw_path)
        transform.main()
        validate.main()  
        load.main(parquet_path, table_name, n_rows, key_cols)


if __name__ == "__main__":
    main()