import csv
import re

input_file = 'input.csv'  # Path to your input CSV file
output_file = 'output.csv'  # Path to the output CSV file

def extract_data_from_row(row):
    # Define a regular expression to extract the desired parts from the 5th column
    match = re.search(r'URI="([^"]+)"Query="[^"]*pyActivity=([^&]+)&[^"]*PreActivity=([^&]+)', row[4])
    if match:
        # Extract URL, pyActivity, and PreActivity
        return match.group(1), match.group(2), match.group(3)
    return '', '', ''

def process_csv(input_file, output_file):
    with open(input_file, 'r', newline='') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Skip the original first row
        next(reader)

        # Write the new header
        writer.writerow(['URL', 'pyActivity', 'PreActivity', 'ResponseTime', '#DBCalls', '#API Calls'])

        stop_processing = False
        rows_to_write = []

        for row in reader:
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
                    continue

            # Check if the row is 'Event' to trigger the special processing
            if not stop_processing and row[0] == 'Event':
                event_found = True
                # Save the current position of the reader
                current_position = infile.tell()
                # Find the next row with 'Thread.run'
                for subsequent_row in reader:
                    if 'Thread.run' in subsequent_row:
                        # Extract the data from the row
                        url, py_activity, pre_activity = extract_data_from_row(subsequent_row)
                        response_time = subsequent_row[2]  # Assuming this is the response time
                        # Insert the new calculated row
                        calculated_row = [url, py_activity, pre_activity, response_time, '', '']  # Empty strings for #DBCalls and #API Calls
                        rows_to_write.append(calculated_row)
                        break
                # Restore the reader to the saved position
                infile.seek(current_position)

            rows_to_write.append(row)

        # Write all rows at once to preserve order
        writer.writerows(rows_to_write)

process_csv(input_file, output_file)