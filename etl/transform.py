import pandas as pd
import numpy as np
import os

def clean_dataset(df: pd.DataFrame, boolean_cols: list[str]) -> pd.DataFrame:
    # Trim whitespace
    str_cols = df.select_dtypes(include=["object", "string"]).columns
    for col in str_cols:
        df[col] = df[col].str.strip()

    # Replace empty strings and invalid entries with None
    df.replace({"": None, "NA": None, "NaN": None, "None": None}, inplace=True)
    df = df.replace({np.nan: None})
    df = df.replace({pd.NA: None})

    # Map Y/N to booleans
    for col in boolean_cols:
        if col in df.columns:
            df[col] = df[col].map({"Y": True, "N": False, "True": True, "False":False})
            df[col] = df[col].where(df[col].isin([True, False]), None)

    return df

def cast_dtypes(df: pd.DataFrame, dtype_mapping: dict) -> pd.DataFrame:
    df = df.astype(dtype_mapping)
    df = df.where(df.notna(), None)

    return df

def save_processed_dataset(df: pd.DataFrame, parquet_path: str):
    os.makedirs(os.path.dirname(parquet_path), exist_ok=True)
    df.to_parquet(parquet_path, index=False)
    print(f"Processed dataset saved to: {parquet_path}")

def main():
    input_path = "data/raw/gdsc_raw.csv"
    output_path = "data/processed/gdsc_clean.parquet"
    boolean_cols = ["CNA", "Gene Expression", "Methylation"]
    dtype_mapping = {
        "COSMIC_ID": "Int64",
        "DRUG_ID": "Int64",
        "LN_IC50": "float64",
        "AUC": "float64",
        "Z_SCORE": "float64",
        "CELL_LINE_NAME": "string",
        "DRUG_NAME": "string",
        "TCGA_DESC": "category",
        "GDSC Tissue descriptor 1": "category",
        "GDSC Tissue descriptor 2": "category",
        "Cancer Type (matching TCGA label)": "category",
        "Microsatellite instability Status (MSI)": "category",
        "Screen Medium": "category",
        "Growth Properties": "category",
        "CNA": "boolean",
        "Gene Expression": "boolean",
        "Methylation": "boolean",
        "TARGET": "string",
        "TARGET_PATHWAY": "category"
    }

    df = pd.read_csv(input_path)
    df = clean_dataset(df, boolean_cols)
    df = cast_dtypes(df, dtype_mapping)
    save_processed_dataset(df, output_path)

if __name__ == "__main__":
    main()