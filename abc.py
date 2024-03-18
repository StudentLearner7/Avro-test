import csv
import re

input_file = 'input.csv'  # Path to your input CSV file
final_output_file = 'final_output.csv'  # Path to the final output CSV file

def process_csv(input_file, final_output_file):
    with open(input_file, newline='') as infile, open(final_output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Skip the original first row
        next(reader)

        # Write the new header
        writer.writerow(['URL', 'pyActivity', 'PreActivity', 'ResponseTime', '#DBCalls', '#API Calls'])

        rows = list(reader)
        processed_rows = []  # This will store the processed rows with the inserted data

        i = 0
        while i < len(rows):
            row = rows[i]
            # Delete the 2nd column
            del row[1]

            if row[0].startswith('JSP/Servlet'):
                value = row[1].replace(',', '')  # Adjust for the deleted column
                if value.isdigit() and int(value) < 5000:
                    # If condition is met, stop processing further rows
                    break

            if row[0] == 'Event':
                # Initialize extracted values
                extracted_url = ''
                extracted_py_activity = ''
                extracted_pre_activity = ''
                response_time = ''

                # Find the next row with 'Thread.run'
                j = i + 1
                while j < len(rows) and 'Thread.run' not in rows[j]:
                    j += 1

                if j < len(rows):
                    # Assuming the 5th column of the row contains the URL and activities
                    match = re.search(r'URI="([^"]+)"Query="[^"]*pyActivity=([^&]+)&[^"]*PreActivity=([^&]+)', rows[j][4])
                    if match:
                        extracted_url = match.group(1)
                        extracted_py_activity = match.group(2)
                        extracted_pre_activity = match.group(3)
                        response_time = rows[j][2]  # Assuming the 3rd column contains the response time

                    # Create the new row to insert before the 'Event' row
                    new_row = [extracted_url, extracted_py_activity, extracted_pre_activity, response_time, '', '']
                    processed_rows.append(new_row)

                # Move the index to the row after 'Thread.run'
                i = j

            processed_rows.append(row)
            i += 1

        # Write all processed rows to the output file
        writer.writerows(processed_rows)

process_csv(input_file, final_output_file)
