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

def calculate_db_calls(rows, start_index):
    count = 0
    for row in rows[start_index + 1:]:
        if row[0].startswith('SQL'):
            count += 1
        elif row[0] == 'Event':
            break
    return count

def insert_calculated_rows(intermediate_output_file, final_output_file):
    with open(intermediate_output_file, newline='') as infile, open(final_output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Write the header
        writer.writerow(next(reader))

        rows = list(reader)
        for i, row in enumerate(rows):
            if row[0] == 'Event':
                db_calls_count = calculate_db_calls(rows, i)  # Count #DBCalls from this 'Event' to the next 'Event'
                if i + 1 < len(rows) and 'Thread.run' in rows[i + 1][3]:
                    data_row = rows[i + 1]
                    extracted_url = re.search(r'URI="([^"]*)"', data_row[4]).group(1) if re.search(r'URI="([^"]*)"', data_row[4]) else 'NA'
                    extracted_py_activity = re.search(r'pyActivity=([^&]*)', data_row[4]).group(1) if re.search(r'pyActivity=([^&]*)', data_row[4]) else 'NA'
                    extracted_pre_activity = re.search(r'PreActivity=([^&]*)', data_row[4]).group(1) if re.search(r'PreActivity=([^&]*)', data_row[4]) else 'NA'
                    response_time = data_row[2]

                    calculated_row = [extracted_url, extracted_py_activity, extracted_pre_activity, response_time, db_calls_count, '']  # Assuming '' for #API Calls
                    writer.writerow(calculated_row)
                    
            writer.writerow(row)

# Define your file paths
input_file = 'input.csv'
intermediate_output_file = 'output.csv'
final_output_file = 'final_output.csv'

# Run the processing functions
process_initial_csv(input_file, intermediate_output_file)
insert_calculated_rows(intermediate_output_file, final_output_file)
