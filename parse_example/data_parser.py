import requests
import pandas as pd

def fetch_api_data(url: str) -> dict:
    """Fetch JSON data from the given API URL."""
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def load_to_dataframe(data: dict) -> pd.DataFrame:
    """Convert 'results' JSON list into a Pandas DataFrame."""
    return pd.DataFrame(data["results"])

def parse_and_transform(df: pd.DataFrame) -> pd.DataFrame:
    """Select and transform key fields only."""
    cols = [c for c in ["effective_time", "id", "set_id", "active_ingredient", "purpose", "warnings"] if c in df.columns]
    df = df[cols].copy()

    # Types
    if "effective_time" in df.columns:
        df["effective_time"] = pd.to_datetime(df["effective_time"], errors="coerce")
    for c in ["id", "set_id"]:
        if c in df.columns:
            df[c] = df[c].astype(str)
    for c in ["active_ingredient", "purpose", "warnings"]:
        if c in df.columns:
            df[c] = df[c].astype(str)

    return df

def save_dataset(df: pd.DataFrame, path: str) -> None:
    """Save dataset locally"""
    df.to_csv(path, index=False, encoding="utf-8")
    print(f"Saved locally: {path}")

def main():
    url = "https://api.fda.gov/drug/label.json?limit=100"

    # Extract
    data = fetch_api_data(url)
    print("Top-level keys:", list(data.keys()))
    print("Number of results:", len(data["results"]))

    # Load
    df = load_to_dataframe(data)
    print("\nColumns in DataFrame:")
    print(df.columns)

    # Parse + Transform
    df_parsed = parse_and_transform(df)

    # Preview output
    print("\nParsed preview (first 10 rows):")
    print(df_parsed.head(10))

    # Save locally
    save_dataset(df_parsed, "parse_example/drug_labels_parsed.csv")

if __name__ == "__main__":
    main()