import csv
import re

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

def insert_calculated_rows(intermediate_output_file, final_output_file):
    with open(intermediate_output_file, newline='') as infile, open(final_output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Write the header
        writer.writerow(next(reader))  # Assumes the first row is the header

        rows = list(reader)
        for i, row in enumerate(rows):
            if row[0] == 'Event':
                if i + 1 < len(rows) and 'Thread.run' in rows[i + 1][3]:
                    data_row = rows[i + 1]
                    # Adjusted regex pattern to match the sample provided
                    match = re.search(r'URI="([^"]*)"Query="pyActivity=([^&]*)&.*?PreActivity=([^&]*)&', data_row[4])
                    if match:
                        extracted_url = match.group(1)
                        extracted_py_activity = match.group(2)
                        extracted_pre_activity = match.group(3)
                        response_time = data_row[2]  # Assuming the response time is in the third column
                        # Insert the new calculated row
                        calculated_row = [extracted_url, extracted_py_activity, extracted_pre_activity, response_time, '', '']
                        writer.writerow(calculated_row)
            writer.writerow(row)

# File paths
input_file = 'input.csv'
intermediate_output_file = 'output.csv'
final_output_file = 'final_output.csv'

# Run the processing functions
process_initial_csv(input_file, intermediate_output_file)
insert_calculated_rows(intermediate_output_file, final_output_file)
