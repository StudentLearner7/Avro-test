import csv
import re

# Define the input CSV and output CSV file paths
input_csv = 'input.csv'
intermediate_output_csv = 'output.csv'  # Intermediate file after initial processing
final_output_csv = 'final_output.csv'  # Final output file with inserted rows

# Process the original CSV to create an intermediate CSV file
def process_csv(input_csv, intermediate_output_csv):
    # ... (same as before)

# This function assumes 'Event' rows are followed by a row that contains the data to extract.
def insert_rows_before_event(intermediate_output_csv, final_output_csv):
    with open(intermediate_output_csv, newline='') as infile, open(final_output_csv, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Write the header to the final output file
        writer.writerow(next(reader))  # Assumes the first row is the header

        # Initialize a placeholder for the previously processed row
        previous_row = None

        for row in reader:
            if row[0] == 'Event' and previous_row:
                # Extract data using regex from the 5th column of the previous row
                data_match = re.search(r'URI="([^"]+)"Query="[^"]*pyActivity=([^&]+)&.*?PreActivity=([^&]+)', previous_row[4])
                if data_match:
                    # Extracted values from the regex groups
                    extracted_url = data_match.group(1)
                    extracted_py_activity = data_match.group(2)
                    extracted_pre_activity = data_match.group(3)
                    # Response time assumed to be in the 3rd column of the 'Thread.run' row
                    response_time = previous_row[2]
                    # Insert the new row with extracted values
                    new_row = [extracted_url, extracted_py_activity, extracted_pre_activity, response_time, '', '']  # Empty strings for #DBCalls and #API Calls
                    writer.writerow(new_row)

            # Write the current row and update the previous row placeholder
            writer.writerow(row)
            previous_row = row

# First, process the original CSV to create an intermediate CSV file
process_csv(input_csv, intermediate_output_csv)

# Then, insert calculated rows before 'Event' rows in the intermediate CSV to create the final output CSV
insert_rows_before_event(intermediate_output_csv, final_output_csv)
