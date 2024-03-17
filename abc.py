import csv

input_file = 'input.csv'  # Path to your input CSV file
output_file = 'output.csv'  # Path to the output CSV file

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

            # Before processing further, check if the row meets the "JSP/Servelet" condition
            if row[0].startswith('JSP/Servelet'):
                value = row[1].replace(',', '')  # Adjust for the deleted column
                if value.isdigit() and int(value) < 5000:
                    # If condition is met, mark to stop processing further rows
                    stop_processing = True
                    continue  # Skip this row and don't process further

            # Insert a new row before rows meeting specific criteria
            if not stop_processing and row[0].startswith('JSP') and len(row) > 2 and row[2] == 'Thread.run':
                new_row = ['Event', 'Time(ms)', 'Thread', 'Stack Trace', 'Detail', 'Level']
                writer.writerow(new_row)

            writer.writerow(row)

process_csv(input_file, output_file)
