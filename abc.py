import csv

input_file = 'input.csv'  # Path to your input CSV file
output_file = 'output.csv'  # Path to the intermediate output CSV file
final_output_file = 'final_output.csv'  # Path to the final output CSV file

def process_csv(input_file, output_file):
    with open(input_file, newline='') as infile, open(output_file, 'w', newline='') as outfile:
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
                    continue

            # Insert a new row before rows meeting specific criteria
            if not stop_processing and row[0].startswith('JSP') and len(row) > 3 and row[3] == 'Thread.run':
                new_row = ['Event', 'Time(ms)', 'Thread', 'Stack Trace', 'Detail', 'Level']
                writer.writerow(new_row)

            writer.writerow(row)

# Apply the first function to process the CSV and create an output file
process_csv(input_file, output_file)

def insert_rows_before_event(output_file, final_output_file):
    with open(output_file, newline='') as infile, open(final_output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Write the new header
        writer.writerow(next(reader))  # Assumes the first row is the header

        rows = list(reader)
        for i, row in enumerate(rows):
            # Check for 'Event' and insert the new calculated row before it
            if row[0] == 'Event':
                # Assuming the previous row contains the data needed for calculation
                # Insert your logic here to calculate values from the previous row if needed
                calculated_row = ['URL', 'pyActivity', 'PreActivity', 'ResponseTime', '#DBCalls', '#API Calls']
                writer.writerow(calculated_row)
            writer.writerow(row)

# Apply the second function to insert a row before each 'Event' record
insert_rows_before_event(output_file, final_output_file)
