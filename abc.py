import csv
import re

# Adjustments are made here for clarity and correction
def insert_calculated_rows(intermediate_output_file, final_output_file):
    with open(intermediate_output_file, newline='') as infile, open(final_output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Write the header
        writer.writerow(next(reader))  # Assumes the first row is the header

        rows = list(reader)
        for i, row in enumerate(rows):
            if row[0] == 'Event':
                # Check if the next row exists and "Thread.run" is in the correct column
                if i + 1 < len(rows) and 'Thread.run' in rows[i + 1][3]:  # Now checking the 4th column after deletion
                    data_row = rows[i + 1]
                    # Use regex to extract the necessary values from the data row
                    match = re.search(r'URI="([^"]*)".*pyActivity=([^&]*)&.*PreActivity=([^&]*)&', data_row[4])
                    if match:
                        extracted_url = match.group(1)
                        extracted_py_activity = match.group(2)
                        extracted_pre_activity = match.group(3)
                        response_time = data_row[2]  # Assuming the response time is in the third column
                        # Insert the new calculated row before the 'Event' row
                        calculated_row = [extracted_url, extracted_py_activity, extracted_pre_activity, response_time, '', '']
                        writer.writerow(calculated_row)
            writer.writerow(row)

# Ensure you've already defined and called `process_initial_csv` function correctly
process_initial_csv(input_file, intermediate_output_file)

# Then, insert calculated rows based on the corrected logic
insert_calculated_rows(intermediate_output_file, final_output_file)
