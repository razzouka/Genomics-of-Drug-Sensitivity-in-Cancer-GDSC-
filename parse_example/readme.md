# Parse Example: OpenFDA Drug Label

This example demonstrates how to parse biomedical data from the [OpenFDA Drug Label API](https://open.fda.gov/apis/drug/label/) using Python and Pandas.  

---

## Files
- `data_parser.py` → Python script that fetches, parses, and transforms the dataset.
- `README.md` → Documentation for this example.
- `screenshots/` → Screenshot of the terminal output preview.
- `drug_labels_parsed.csv` → Local output folder (ignored by Git).

---

## Steps Performed in `data_parser.py`

1. **Define the API endpoint**  
   - URL: `https://api.fda.gov/drug/label.json?limit=100`  
   - The `limit` parameter controls how many drug entries are returned.

2. **Extract (fetch API data)**  
   - `fetch_api_data(url)` uses `requests.get()` to retrieve the JSON.  
   - The response is converted into a Python dictionary.

3. **Load (create DataFrame)**  
   - `load_to_dataframe(data)` converts the `"results"` section into a Pandas DataFrame.

4. **Parse and Transform**  
   - `parse_and_transform(df)` selects and cleans key fields:  
     - `effective_time` → converted to `datetime`  
     - `id`, `set_id` → converted to `string`  
     - `active_ingredient`, `purpose`, `warnings` → converted to `string`

5. **Preview output**  
   - Prints the first 10 rows of the parsed dataset for clarity.

6. **Save locally (optional)**  
   - `save_local(df, "parse_example/drug_labels_parsed.csv")` saves the dataset to a local folder.  
   - The file is excluded from Git via `.gitignore`.

---

## 📊 Output

Below is an example of the output preview:

![Drug_label_parser](parse_output1.png)(parse_output2.png)

The full parsed dataset is saved locally in `parse_example/` (ignored by Git).