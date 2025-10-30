import pandas as pd

def check_no_duplicates(df: pd.DataFrame, key_cols: list[str]):
    if df.duplicated(subset=key_cols).any():
        raise ValueError(f"Duplicate rows found for key columns: {key_cols}")

def check_boolean_columns(df: pd.DataFrame, boolean_cols: list[str]):
    for col in boolean_cols:
        if col in df.columns:
            invalid = df[~df[col].isin([True, False]) & df[col].notna()]
            if not invalid.empty:
                raise ValueError(f"Column '{col}' has non-boolean values.")

def check_dtype(df: pd.DataFrame, dtype_mapping: dict):
    for col, dtype in dtype_mapping.items():
        if col in df.columns:
            if not pd.api.types.is_dtype_equal(df[col].dtype, dtype):
                raise TypeError(f"Column '{col}' has dtype {df[col].dtype}, expected {dtype}")

def check_no_missing(df: pd.DataFrame, critical_cols: list[str]):
    missing = df[critical_cols].isna().any()
    if missing.any():
        cols = missing[missing].index.tolist()
        raise ValueError(f"Missing values found in critical columns: {cols}")
    
def main():
    # 1. Load processed dataset
    parquet_path = "data/processed/gdsc_clean.parquet"
    df = pd.read_parquet(parquet_path)

    # 2. Define variables for validation
    boolean_cols = ["CNA", "Gene Expression", "Methylation"]
    critical_cols = ["COSMIC_ID", "DRUG_ID", "LN_IC50", "AUC", "Z_SCORE"]
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

    # 3. Run validations
    check_no_duplicates(df, key_cols=["COSMIC_ID", "DRUG_ID"])
    check_boolean_columns(df, boolean_cols)
    check_dtype(df, dtype_mapping)
    check_no_missing(df, critical_cols)

    print("All validations passed successfully!")

if __name__ == "__main__":
    main()