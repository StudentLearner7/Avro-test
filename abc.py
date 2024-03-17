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

        # Convert reader to list for better control over iterations
        rows = list(reader)
        for i, row in enumerate(rows):
            # Delete the 2nd column
            del row[1]

            # Check if the row starts with "JSP/Servelet" and has a numeric value less than 5000 in the adjusted 2nd column
            if row[0].startswith('JSP/Servelet'):
                value = row[1].replace(',', '')  # Adjust for the deleted column, making the original 3rd column now the 2nd
                if value.isdigit() and int(value) < 5000:
                    # If condition is met, stop processing further, excluding this and all subsequent rows
                    break  # Break from the loop to stop processing

            # Insert a new row before any row that starts with "JSP" and where the adjusted 4th column (now 3rd) is "Thread.run"
            if row[0].startswith('JSP') and len(row) > 2 and row[2] == 'Thread.run':  # Adjust column index for "Thread.run" check
                new_row = ['Event', 'Time(ms)', 'Thread', 'Stack Trace', 'Detail', 'Level']
                writer.writerow(new_row)  # Write the new row before the current row

            writer.writerow(row)

            if row[0].startswith('JSP/Servelet') and value.isdigit() and int(value) < 5000:
                # Stop writing to file after adding all necessary rows before the condition is met
                break

process_csv(input_file, output_file)
