import csv
from urllib.parse import parse_qs, urlparse

input_file = 'input.csv'  # Path to your input CSV file
output_file = 'output.csv'  # Path to the output CSV file

def extract_data(query_string):
    """Extract URL, pyActivity, and PreActivity from the query string."""
    parsed_url = urlparse(query_string)
    qs_data = parse_qs(parsed_url.query)
    url = parsed_url.path
    py_activity = qs_data.get('pyActivity', [''])[0]
    pre_activity = qs_data.get('PreActivity', [''])[0]
    return url, py_activity, pre_activity

def process_csv(input_file, output_file):
    with open(input_file, newline='') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Skip the original first row
        next(reader)

        # Write the new header
        writer.writerow(['URL', 'pyActivity', 'PreActivity', 'ResponseTime', '#DBCalls', '#API Calls'])

        rows = list(reader)
        stop_processing = False
        i = 0
        while i < len(rows):
            row = rows[i]

            if stop_processing:
                break

            # Delete the 2nd column
            del row[1]

            # Before processing further, check if the row meets the "JSP/Servlet" condition
            if row[0].startswith('JSP/Servlet'):
                value = row[1].replace(',', '')  # Adjust for the deleted column
                if value.isdigit() and int(value) < 5000:
                    # If condition is met, mark to stop processing further rows
                    stop_processing = True
                    i += 1
                    continue  # Skip this row and don't process further

            if not stop_processing and row[0] == 'Event':
                # Look ahead to the next row for 'Thread.run'
                if i+1 < len(rows) and 'Thread.run' in rows[i+1]:
                    next_row = rows[i+1]
                    # Extract the required values from the 5th column
                    url, py_activity, pre_activity = extract_data(next_row[4])
                    response_time = next_row[2]
                    # Insert a new calculated row
                    new_row = [url, py_activity, pre_activity, response_time, '', '']
                    writer.writerow(new_row)

            # Write the current row
            writer.writerow(row)
            i += 1

process_csv(input_file, output_file)
