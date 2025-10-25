import pandas as pd
import os

# === 1. Download and load the dataset from Google Sheets ===
FILE_ID = "1vsEQF1diDzx3ZFRYYzCPDXJC2bqpjWMV"
file_url = f"https://docs.google.com/spreadsheets/d/{FILE_ID}/export?format=csv"

raw_data = pd.read_csv(file_url)

# === 2. Inspect dataset ===
print("First 10 rows:")
print(raw_data.head(10))
print("\nShape:", raw_data.shape)
print("\nColumns:", raw_data.columns.tolist())
print("\nDtypes before cleaning:\n", raw_data.dtypes)

# === 3. Clean missing values and whitespaces ===
raw_data = raw_data.applymap(lambda x: x.strip() if isinstance(x, str) else x)
raw_data.replace({"": pd.NA, "NA": pd.NA, "NaN": pd.NA, "None": pd.NA}, inplace=True)

# === 4. Data type casting ===
raw_data = raw_data.astype({
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
    "CNA": "category",            
    "Gene Expression": "category",
    "Methylation": "category",    
    "TARGET": "string",           
    "TARGET_PATHWAY": "category"
})

print("\nDtypes after casting:\n", raw_data.dtypes)

# === 5. Save cleaned dataset as CSV and Parquet ===
os.makedirs("data", exist_ok=True)

csv_path = "data/gdsc_clean.csv"
parquet_path = "data/gdsc_clean.parquet"

raw_data.to_csv(csv_path, index=False)
raw_data.to_parquet(parquet_path, index=False)

print(f"\nSaved cleaned dataset to:\n - {csv_path}\n - {parquet_path}")

# === 6. Verify saved file ===
reloaded = pd.read_parquet(parquet_path)
print("\nReloaded dataset info:")
print(reloaded.info())
print(reloaded.head(10))