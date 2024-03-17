import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

input_file = 'input.csv'  # Path to your input CSV file
output_excel_file = 'output.xlsx'  # Path to the output Excel file

def process_csv_and_create_excel(input_file, output_excel_file):
    # Read the CSV, skipping the first row (header) from the original file
    df = pd.read_csv(input_file, skiprows=1, header=None)

    # Delete the 2nd column
    df.drop(1, axis=1, inplace=True)

    # Define the new header
    new_header = ['URL', 'pyActivity', 'PreActivity', 'ResponseTime', '#DBCalls', '#API Calls']
    
    # Adjust the header based on the number of columns in df
    df.columns = new_header[:df.shape[1]]

    # Find the index where "JSP/Servlet" rows with value in the second column less than 5000
    stop_index = None
    for index, row in df.iterrows():
        if row['URL'].startswith('JSP/Servlet'):
            value = int(row['pyActivity'].replace(',', ''))
            if value < 5000:
                stop_index = index
                break

    # If such a row is found, keep only the rows before it
    if stop_index is not None:
        df = df.iloc[:stop_index]

    # Initialize an Excel writer with openpyxl engine
    writer = pd.ExcelWriter(output_excel_file, engine='openpyxl')
    df.to_excel(writer, index=False, sheet_name='Sheet1')  # Write the DataFrame to an Excel file
    writer.save()

    # Apply grouping using openpyxl
    wb = writer.book
    ws = wb.active

    # Initialize variables for grouping logic
    group_start = None
    for idx, row in enumerate(ws.iter_rows(min_row=2, max_col=1, values_only=True), start=2):
        if row[0] == 'Event':
            if group_start is not None:
                ws.row_dimensions.group(group_start, idx - 1, hidden=True)
            group_start = idx

    # Final group to the end
    if group_start is not None:
        ws.row_dimensions.group(group_start, ws.max_row, hidden=True)

    wb.save(output_excel_file)

process_csv_and_create_excel(input_file, output_excel_file)
