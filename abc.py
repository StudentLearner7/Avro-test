import csv

input_file = 'input.csv'  # Path to your input CSV file
output_file = 'output.csv'  # Path to the updated output CSV file

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
            
            # Before processing further, check if the row starts with "JSP/Servelet" and meets the deletion criteria
            if row[0].startswith('JSP/Servelet'):
                value = row[1].replace(',', '')  # Adjusted index due to column deletion
                if value.isdigit() and int(value) < 5000:
                    # If condition met, stop processing further, excluding this and subsequent rows
                    return

            # Now, insert a new row before any row that meets the new row insertion criteria
            if row[0].startswith('JSP') and len(row) > 2 and row[3] == 'Thread.run':
                new_row = ['Event', 'Time(ms)', 'Thread', 'Stack Trace', 'Detail', 'Level']
                writer.writerow(new_row)

            writer.writerow(row)

process_csv(input_file, output_file)
