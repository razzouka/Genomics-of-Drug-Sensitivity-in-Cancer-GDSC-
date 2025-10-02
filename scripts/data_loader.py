import pandas as pd
import wget
#URL_to_my_dataset
FILE_ID = "1vsEQF1diDzx3ZFRYYzCPDXJC2bqpjWMV"
file_url = f"https://docs.google.com/spreadsheets/d/{FILE_ID}/export?format=csv"
#load_the_data
raw_data = pd.read_csv(file_url)
#show_the_first_10_rows
print(raw_data.head(10))
#show_number_of_rows_and_columns
print("Shape:", raw_data.shape)
#show_list_of_features
print("Columns:", raw_data.columns.tolist())
#show_data_type_of_each_column
print("Dtypes:\n", raw_data.dtypes)
#clean_the_missing_values
raw_data = raw_data.applymap(lambda x: x.strip() if isinstance(x, str) else x)
raw_data.replace({"": pd.NA, "NA": pd.NA, "NaN": pd.NA, "None": pd.NA}, inplace=True)
#data_type_casting
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
#show_data_types_after_casting
print("Dtypes after casting:\n", raw_data.dtypes)
import os
os.makedirs("data", exist_ok=True)
#save_cleaned_dataset_as_csv
raw_data.to_csv("data/gdsc_clean.csv", index=False)
print("Saved cleaned dataset to data/gdsc_clean.csv")
#check_reproducibility 
raw_data_reloaded = pd.read_csv("data/gdsc_clean.csv")
raw_data_reloaded = raw_data_reloaded.astype({
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
print("\nReloaded dataset info:")
print(raw_data_reloaded.info())  
print(raw_data_reloaded.head(10)) 