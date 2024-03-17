import pandas as pd
from openpyxl import load_workbook

# Input and output file paths
input_file = 'input.csv'
output_excel_file = 'output.xlsx'

# Read the CSV, skip the first original row, and manually set new column headers
df = pd.read_csv(input_file, skiprows=1, header=None)
new_columns = ['URL', 'pyActivity', 'PreActivity', 'ResponseTime', '#DBCalls', '#API Calls']
df.columns = new_columns[:len(df.columns)-1] + df.columns[len(df.columns)-1:].tolist()  # Adjust for deleted column

# Delete the 2nd column
df.drop(df.columns[1], axis=1, inplace=True)

# Find the rows to stop processing at (first column starts with "JSP/Servlet" and value < 5000 in the now second column)
stop_index = None
for index, row in df.iterrows():
    if row[0].startswith('JSP/Servlet'):
        value = int(row[1].replace(',', ''))
        if value < 5000:
            stop_index = index
            break

# If a stop index is found, truncate the dataframe up to that point
if stop_index is not None:
    df = df.loc[:stop_index-1]

# Save processed DataFrame to Excel
df.to_excel(output_excel_file, index=False)

# Now use openpyxl for adding groupings
wb = load_workbook(output_excel_file)
ws = wb.active

event_rows = [row[0].row for row in ws if row[0].value == 'Event']
for start, end in zip(event_rows, event_rows[1:] + [ws.max_row]):
    ws.row_dimensions.group(start + 1, end - 1, hidden=True)

wb.save(output_excel_file)
