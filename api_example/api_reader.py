import requests
import pandas as pd

# Define the API endpoint
url = "https://api.fda.gov/drug/label.json?limit=100"

# Send GET request to fetch data from the API
response = requests.get(url)

# Convert data to a python dictionary
data = response.json()

# Explore the structure of JSON
print("Top-level keys:", data.keys()) 
print("Number of results:", len(data["results"]))

# Check which feilds exist
print("First entry keys:", data["results"][0].keys()) 

# Convert results to into a dataframe
df = pd.json_normalize(data["results"])

# Explore the available columns
print("\nColumns in DataFrame:")
print(df.columns)

# show the selected columns
print("\nSelected columns:")
print(df[["active_ingredient", "purpose", "warnings"]].head(100))
