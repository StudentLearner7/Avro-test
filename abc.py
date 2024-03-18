import csv
import re

input_file = 'input.csv'  # Path to your input CSV file
intermediate_output_file = 'intermediate_output.csv'  # Path to the intermediate output CSV file
final_output_file = 'final_output.csv'  # Path to the final output CSV file

def process_csv(input_file, intermediate_output_file):
    with open(input_file, newline='') as infile, open(intermediate_output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Skip the original first row
        next(reader)

        # Write the new header
        writer.writerow(['URL', 'pyActivity', 'PreActivity', 'ResponseTime', '#DBCalls', '#API Calls'])

        stop_processing = False

        for row in list(reader):
            if stop_processing:
                break

            # Delete the 2nd column
            del row[1]

            # Check if the row meets the "JSP/Servlet" condition
            if row[0].startswith('JSP/Servlet'):
                value = row[1].replace(',', '')  # Adjust for the deleted column
                if value.isdigit() and int(value) < 5000:
                    # If condition is met, mark to stop processing further rows
                    stop_processing = True
                    continue  # Skip this row and don't process further

            # Insert a new row before rows meeting specific criteria
            if not stop_processing and row[0].startswith('JSP') and len(row) > 3 and row[3] == 'Thread.run':
                new_row = ['Event', 'Time(ms)', 'Thread', 'Stack Trace', 'Detail', 'Level']
                writer.writerow(new_row)

            writer.writerow(row)

def insert_rows_before_event(intermediate_output_file, final_output_file):
    with open(intermediate_output_file, newline='') as infile, open(final_output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Write the header
        writer.writerow(next(reader))  # Assumes the first row is the header

        previous_row = None  # Initialize the previous row variable

        for row in reader:
            # Check for 'Event' row and previous row presence
            if row[0] == 'Event' and previous_row:
                # Use regex to extract the necessary values from the previous row
                regex_search = re.search(r'URI="([^"]+)"Query=".*?pyActivity=([^&]+)&.*?PreActivity=([^&]+)&.*"', previous_row[4])
                if regex_search:
                    extracted_url = regex_search.group(1)
                    extracted_py_activity = regex_search.group(2)
                    extracted_pre_activity = regex_search.group(3)
                    response_time = previous_row[2]  # Assuming the response time is in the third column
                    # Create and write the new row
                    calculated_row = [extracted_url, extracted_py_activity, extracted_pre_activity, response_time, '', '']  # Empty strings for #DBCalls and #API Calls
                    writer.writerow(calculated_row)
            writer.writerow(row)
            # Update the previous row
            previous_row = row

# Run the two processing functions sequentially
process_csv(input_file, intermediate_output_file)
insert_rows_before_event(intermediate_output_file, final_output_file)
