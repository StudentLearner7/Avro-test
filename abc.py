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
            # Delete the 2nd column from the original CSV (which becomes the 1st column after deletion)
            modified_row = row[:1] + row[2:]

            # Check if the row should stop the process based on your conditions
            if modified_row[0].lower().startswith('jsp/servlet'):
                # Check if the value is less than 5000, considering comma removal
                value = modified_row[1].replace(',', '')
                if value.isdigit() and int(value) < 5000:
                    break  # Stop processing further rows once condition is met

            writer.writerow(modified_row)

process_csv(input_file, output_file)
