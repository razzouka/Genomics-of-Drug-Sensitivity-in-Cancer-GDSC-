import requests
import pandas as pd

# Extract data from the API and convert it to a python dictionary
url = "https://api.fda.gov/drug/label.json?limit=100"
response = requests.get(url)
data = response.json()

# Explore the structure of JSON
print("\nTop-level keys:", data.keys()) 
print("\nNumber of results:", len(data["results"]))

# Load data into a dataframe
df = pd.DataFrame(data["results"])

# Check which feilds exist
print("\nFirst entry keys:", data["results"][0].keys())

# Explore the available columns
print("\nColumns in DataFrame:")
print(df.columns)

# show the selected columns (no flattening)
print("\nSelected columns:")
print(df[["active_ingredient", "purpose", "warnings"]].head(100))
