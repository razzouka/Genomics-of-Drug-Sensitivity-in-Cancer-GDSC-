import os
import pandas as pd

def load_dataset(file_id: str) -> pd.DataFrame:
    file_url = f"https://docs.google.com/spreadsheets/d/{file_id}/export?format=csv"
    df = pd.read_csv(file_url)
    print(f"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    return df

def save_raw_data(df: pd.DataFrame, output_path: str):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Raw data saved to: {output_path}")

def main(file_id: str, output_path: str):
    df = load_dataset(file_id)
    save_raw_data(df, output_path)