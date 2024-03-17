import pandas as pd

# Correct path for input CSV and output Excel file
input_file = 'input.csv'
output_excel_file = 'output.xlsx'

# Load the CSV file, skipping the first row as it's original headers
df = pd.read_csv(input_file, skiprows=1, header=None)

# Define new headers, after considering the deletion of the 2nd column
new_headers = ['URL', 'pyActivity', 'PreActivity', 'ResponseTime', '#DBCalls', '#API Calls']
df.drop(columns=[1], inplace=True)  # Delete the 2nd column
df.columns = new_headers[:len(df.columns)]  # Reassign new headers

# Apply the logic to stop processing at a specific row
for i, row in df.iterrows():
    if row['URL'].startswith('JSP/Servlet'):
        try:
            # Assuming the value is now in the 'PreActivity' column after deletion
            value = int(row['PreActivity'].replace(',', ''))
            if value < 5000:
                df = df.iloc[:i]  # Keep rows up to but not including the current one
                break
        except ValueError:
            # In case conversion to int fails, ignore and continue
            continue

# Save the modified DataFrame to an Excel file
df.to_excel(output_excel_file, index=False)

# Now, apply grouping using openpyxl
from openpyxl import load_workbook

wb = load_workbook(output_excel_file)
ws = wb.active

# Assuming 'Event' is in the 'URL' column, identify rows needing grouping
event_rows = [cell.row for cell in ws['A'] if cell.value == 'Event']
for start, end in zip(event_rows, event_rows[1:] + [ws.max_row + 1]):
    ws.row_dimensions.group(start + 1, end - 1, hidden=True)

wb.save(output_excel_file)
