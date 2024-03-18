import csv
import re

# Process the original CSV and create an intermediate CSV file.
def process_initial_csv(input_file, intermediate_output_file):
    with open(input_file, newline='') as infile, open(intermediate_output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Skip the original first row and write the new header
        next(reader)
        writer.writerow(['URL', 'pyActivity', 'PreActivity', 'ResponseTime', '#DBCalls', '#API Calls'])

        stop_processing = False

        for row in reader:
            if stop_processing:
                break

            # Delete the 2nd column
            del row[1]

            # Check if the row meets the "JSP/Servlet" condition
            if row[0].startswith('JSP/Servlet'):
                value = row[1].replace(',', '')
                if value.isdigit() and int(value) < 5000:
                    stop_processing = True
                    continue

            # Insert a placeholder row before rows meeting specific criteria
            if not stop_processing and row[0].startswith('JSP') and 'Thread.run' in row:
                placeholder_row = ['Event', 'Time(ms)', 'Thread', 'Stack Trace', 'Detail', 'Level']
                writer.writerow(placeholder_row)

            writer.writerow(row)

# Apply a second processing step on the intermediate CSV to insert calculated rows before 'Event' rows.
def insert_calculated_rows(intermediate_output_file, final_output_file):
    with open(intermediate_output_file, newline='') as infile, open(final_output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Write the header
        writer.writerow(next(reader))  # Assumes the first row is the header

        # Initialize a list to keep track of the rows
        rows = list(reader)
        for i, row in enumerate(rows):
            if row[0] == 'Event':
                # Check for the row after the Event row where the data should be extracted
                if i + 1 < len(rows) and 'Thread.run' in rows[i + 1]:
                    data_row = rows[i + 1]
                    # Use regex to extract the necessary values from the data row
                    match = re.search(r'URI="([^"]*)".*?pyActivity=([^&]*)&.*?PreActivity=([^&]*)&', data_row[4])
                    if match:
                        extracted_url = match.group(1)
                        extracted_py_activity = match.group(2)
                        extracted_pre_activity = match.group(3)
                        # Response time is assumed to be in the third column
                        response_time = data_row[2]
                        # Insert the new calculated row
                        calculated_row = [extracted_url, extracted_py_activity, extracted_pre_activity, response_time, '', '']  # Assuming empty for #DBCalls and #API Calls
                        writer.writerow(calculated_row)
            writer.writerow(row)

# Define your file paths
input_file = 'input.csv'
intermediate_output_file = 'output.csv'
final_output_file = 'final_output.csv'

# Run the first processing function
process_initial_csv(input_file, intermediate_output_file)

# Then, run the second processing function to insert the calculated rows
insert_calculated_rows(intermediate_output_file, final_output_file)
