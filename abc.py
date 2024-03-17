import csv

input_file = 'input.csv'  # Path to your input CSV file
output_file = 'output.csv'  # Path to your output CSV file

def process_csv(input_file, output_file):
    with open(input_file, newline='') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Skip the original first row
        next(reader)

        # Write the new header
        writer.writerow(['URL', 'pyActivity', 'PreActivity', 'ResponseTime', '#DBCalls', '#API Calls'])

        for row in reader:
            # Delete the 2nd column
            del row[1]

            # Convert the value to integer, considering commas, to check the deletion condition
            if row[0].startswith('JSP/Servelet'):
                value = row[2].replace(',', '')  # Adjusted for the removed column
                if value.isdigit() and int(value) < 5000:
                    # If condition met, stop processing further
                    return

            # Check condition for adding a new row
            if row[0].startswith('JSP') and len(row) > 3 and row[3] == 'Thread.run':
                new_row = ['Event', 'Time(ms)', 'Thread', 'Stack Trace', 'Detail', 'Level']
                writer.writerow(new_row)

            writer.writerow(row)

process_csv(input_file, output_file)
