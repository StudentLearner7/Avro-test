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
    with open(input_file, 'r', newline='') as infile:
        reader = csv.reader(infile)
        data = list(reader)

    # Skip the original first row and write the new header
    data_iter = iter(data[1:])  # Create an iterator skipping the first row
    output_data = [['URL', 'pyActivity', 'PreActivity', 'ResponseTime', '#DBCalls', '#API Calls']]

    stop_processing = False

    while not stop_processing:
        try:
            row = next(data_iter)
        except StopIteration:
            # If there are no more rows to process, break the loop
            break

        # Delete the 2nd column
        del row[1]

        # Check if the row meets the "JSP/Servlet" condition
        if row[0].startswith('JSP/Servlet'):
            value = row[1].replace(',', '')  # Adjust for the deleted column
            if value.isdigit() and int(value) < 5000:
                stop_processing = True
                continue

        # Insert a new row before rows meeting specific criteria
        if row[0] == 'Event':
            # Peek the next row to check for 'Thread.run'
            next_row = next(data_iter)
            if 'Thread.run' in next_row:
                # Extract the data from the next row
                url, py_activity, pre_activity = extract_data_from_row(next_row)
                response_time = next_row[2]  # Assuming this is the response time
                # Insert the new calculated row
                calculated_row = [url, py_activity, pre_activity, response_time, '', '']  # Empty strings for #DBCalls and #API Calls
                output_data.append(calculated_row)
            output_data.append(row)  # Make sure to include the 'Event' row after the new row
            output_data.append(next_row)  # Also include the 'Thread.run' row
        else:
            output_data.append(row)  # Regular row that doesn't require special handling

    # Write all the processed data to the output CSV
    with open(output_file, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(output_data)

process_csv(input_file, output_file)