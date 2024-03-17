import pandas as pd
import csv
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

input_csv = 'input.csv'
output_excel = 'output.xlsx'

def process_csv_to_excel(input_csv, output_excel):
    # Process CSV: read, apply conditions, and filter rows.
    with open(input_csv, newline='') as infile:
        reader = list(csv.reader(infile))
        header = ['URL', 'pyActivity', 'PreActivity', 'ResponseTime', '#DBCalls', '#API Calls']
        rows_to_keep = []
        stop_processing = False

        for i, row in enumerate(reader[1:], start=1):  # Skip original header row
            del row[1]  # Delete 2nd column

            if row[0].startswith('JSP/Servlet'):
                value = int(row[1].replace(',', ''))
                if value < 5000:
                    stop_processing = True
                    break  # Stop adding rows

            if row[0].startswith('JSP') and 'Thread.run' in row:
                # Insert special row before the current row
                special_row = ['Event', 'Time(ms)', 'Thread', 'Stack Trace', 'Detail', 'Level']
                rows_to_keep.append(special_row)

            rows_to_keep.append(row)

        if not stop_processing:
            # If the loop wasn't broken, all rows are processed without encountering the stop condition
            rows_to_keep = reader[1:]  # Re-include all rows if no stop condition met

    # Create a new Excel workbook and sheet
    wb = Workbook()
    ws = wb.active

    # Write new header and rows
    ws.append(header)
    for row in rows_to_keep:
        ws.append(row)

    # Save workbook
    wb.save(output_excel)

process_csv_to_excel(input_csv, output_excel)
