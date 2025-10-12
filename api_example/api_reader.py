import requests
import pandas as pd

# Function: Extract data from API
def fetch_api_data(url: str) -> dict:
    """Fetch JSON data from the given API URL."""
    response = requests.get(url)
    response.raise_for_status()  # Raise error if request fails
    return response.json()

# Function: Load into DataFrame
def load_to_dataframe(data: dict) -> pd.DataFrame:
    """Convert API JSON results into a Pandas DataFrame."""
    return pd.DataFrame(data["results"])

# Function: Transform selected column types
def transform_types(df: pd.DataFrame) -> pd.DataFrame:
    """Apply type transformations to key columns only."""

    # Convert effective_time to datetime
    if "effective_time" in df.columns:
        df["effective_time"] = pd.to_datetime(df["effective_time"], errors="coerce")

    # Ensure IDs are strings
    for col in ["id", "set_id"]:
        if col in df.columns:
            df[col] = df[col].astype(str)

    # Convert selected text fields to string for clean export
    for col in ["active_ingredient", "purpose", "warnings"]:
        if col in df.columns:
            df[col] = df[col].astype(str)

    return df

# Function: Save DataFrame to CSV
def save_dataframe(df: pd.DataFrame, filename: str = "drug_labels.csv") -> None:
    """Save DataFrame to a CSV file."""
    df.to_csv(filename, index=False, encoding="utf-8")
    print(f"Data saved to {filename}")

# Main workflow
def main():
    url = "https://api.fda.gov/drug/label.json?limit=100"

    # Step 1: Extract
    data = fetch_api_data(url)
    print("Top-level keys:", data.keys())
    print("Number of results:", len(data["results"]))

    # Step 2: Load
    df = load_to_dataframe(data)
    print("\nColumns in DataFrame:")
    print(df.columns)

    # Step 3: Transform
    df = transform_types(df)

    # Step 4: Show selected columns
    print("\nSelected columns (first 10 rows):")
    print(df[["active_ingredient", "purpose", "warnings"]].head(10))

    # Step 5: Save
    save_dataframe(df)

# Entry point
if __name__ == "__main__":
    main()