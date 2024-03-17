import pandas as pd

# Define the input CSV and output Excel file paths
input_csv = 'input.csv'
output_excel = 'output.xlsx'

def process_csv_to_excel(input_csv, output_excel):
    # Read the CSV data, skipping the first row
    data = pd.read_csv(input_csv, skiprows=1, header=None)

    # Delete the second column
    data.drop(columns=data.columns[1], inplace=True)

    # Set the new header
    new_header = ['URL', 'pyActivity', 'PreActivity', 'ResponseTime', '#DBCalls', '#API Calls']
    # Ensure the correct number of columns are labeled in case the original CSV had more columns
    data.columns = new_header[:len(data.columns)] + data.columns[len(data.columns):].tolist()

    # Find the index to stop processing if 'JSP/Servlet' value is less than 5000
    stop_index = None
    for index, row in data.iterrows():
        if row[0].startswith('JSP/Servlet'):
            value = int(row[1].replace(',', ''))
            if value < 5000:
                stop_index = index
                break

    # If a stop index was found, truncate the dataframe to stop at that index
    if stop_index is not None:
        data = data.iloc[:stop_index]

    # Write the processed data to an Excel file
    data.to_excel(output_excel, index=False, header=True)

# Call the function to process the CSV and produce an Excel file
process_csv_to_excel(input_csv, output_excel)
