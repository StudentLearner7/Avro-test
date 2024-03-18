import csv
import re

# Function to insert calculated rows before 'Event' rows in the intermediate file
def insert_calculated_rows(intermediate_output_file, final_output_file):
    with open(intermediate_output_file, 'r', newline='') as infile, open(final_output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Directly write the header to the final output
        writer.writerow(next(reader))

        # Convert reader to list for easier manipulation
        rows = list(reader)
        for i, row in enumerate(rows):
            # Check if the current row is an 'Event' row
            if row[0] == 'Event':
                # Check the next row for 'Thread.run' in the correct column (after deletion, now 4th column)
                if i + 1 < len(rows) and 'Thread.run' in rows[i + 1][3]:
                    # Attempt to extract data using regex from the 5th column of the next row
                    data_match = re.search(r'URI="([^"]*)".*?pyActivity=([^&]*)&.*?PreActivity=([^&]*)&', rows[i + 1][4])
                    if data_match:
                        # Extract URL, pyActivity, PreActivity
                        url, py_activity, pre_activity = data_match.groups()
                        # Assume response time is in the 3rd column of the next row
                        response_time = rows[i + 1][2]
                        # Create and insert the new calculated row before the 'Event' row
                        calculated_row = [url, py_activity, pre_activity, response_time, '', '']  # Assuming '' for #DBCalls and #API Calls
                        writer.writerow(calculated_row)
            
            # Write the current row to the final output
            writer.writerow(row)

# Assuming process_initial_csv(input_file, intermediate_output_file) is defined and called as you have done

# Define your file paths
input_file = 'input.csv'
intermediate_output_file = 'intermediate_output.csv'
final_output_file = 'final_output.csv'

# First process the initial CSV to create an intermediate file
# process_initial_csv(input_file, intermediate_output_file)  # Uncomment this if not already called

# Next, enhance the intermediate file with calculated rows
insert_calculated_rows(intermediate_output_file, final_output_file)
