import pandas as pd
import wget
#URL_to_my_dataset
FILE_ID = "1vsEQF1diDzx3ZFRYYzCPDXJC2bqpjWMV"
file_url = f"https://docs.google.com/spreadsheets/d/{FILE_ID}/export?format=csv"
#load_the_data
raw_data = pd.read_csv(file_url)
#show_the_first_10_rows
print(raw_data.head(10))
