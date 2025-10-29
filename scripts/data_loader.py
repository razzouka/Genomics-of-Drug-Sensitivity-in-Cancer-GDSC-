import pandas as pd
import os

# 1. Load dataset from Google Sheets
def load_dataset(file_id: str) -> pd.DataFrame:
    file_url = f"https://docs.google.com/spreadsheets/d/{file_id}/export?format=csv"
    df = pd.read_csv(file_url)
    print(f"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    return df

# 2. Clean dataset
def clean_dataset(df: pd.DataFrame, boolean_cols: list[str]) -> pd.DataFrame:
    # Trim whitespaces for string/object columns
    str_cols = df.select_dtypes(include=["object", "string"]).columns
    for col in str_cols:
        df[col] = df[col].str.strip()
    
    # Standardize missing values
    df.replace({"": pd.NA, "NA": pd.NA, "NaN": pd.NA, "None": pd.NA}, inplace=True)
    
    # Map Y/N to boolean for specified columns
    for col in boolean_cols:
        df[col] = df[col].map({"Y": True, "N": False})
    
    return df

# 3. Cast data types
def cast_dtypes(df: pd.DataFrame, dtype_mapping: dict) -> pd.DataFrame:
    df = df.astype(dtype_mapping)
    return df

# 4. Save cleaned dataset
def save_dataset(df: pd.DataFrame, csv_path: str, parquet_path: str):
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    df.to_csv(csv_path, index=False)
    df.to_parquet(parquet_path, index=False)
    print(f"Saved cleaned dataset to:\n - {csv_path}\n - {parquet_path}")

# 5. Verify saved dataset
def verify_dataset(parquet_path: str) -> pd.DataFrame:
    df = pd.read_parquet(parquet_path)
    print("\nReloaded dataset info:")
    print(df.info())
    print(df.head(10))
    return df

# Main function
def main():
    # Variables 
    file_id = os.environ.get("GDSC_FILE_ID")
    if not file_id:
        raise ValueError("Environment variable GDSC_FILE_ID is not set.")
    
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
    
    csv_path = "data/gdsc_clean.csv"
    parquet_path = "data/gdsc_clean.parquet"

    # Run pipeline
    df = load_dataset(file_id)
    df = clean_dataset(df, boolean_cols)
    df = cast_dtypes(df, dtype_mapping)
    save_dataset(df, csv_path, parquet_path)
    verify_dataset(parquet_path)

if __name__ == "__main__":
    main()