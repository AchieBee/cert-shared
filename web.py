import csv
import re
import random

def fix_csv(input_file, output_file):
    with open(input_file, 'r', newline='', encoding='utf-8') as infile, \
         open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        
        reader = csv.reader(infile)
        writer = csv.writer(outfile, quoting=csv.QUOTE_MINIMAL)
        
        # Write the header row
        header = next(reader)
        writer.writerow(header)
        
        for row in reader:
            # Fix number of fields
            if len(row) < 12:
                row.extend([''] * (12 - len(row)))
            elif len(row) > 12:
                row = row[:12]
            
            # Fix check_radio column (index 8)
            row[8] = row[8].lower().strip()
            if row[8] not in ['radio', 'check']:
                row[8] = random.choice(['radio', 'check'])  # Randomly assign 'radio' or 'check'
            
            # Fix correct_ans column (index 7)
            correct_ans = row[7]
            correct_ans = re.sub(r'[^1-6,]', '', correct_ans)  # Remove invalid characters
            correct_ans = re.sub(r',+', ',', correct_ans)  # Remove duplicate commas
            correct_ans = correct_ans.strip(',')  # Remove leading/trailing commas
            
            # Ensure all numbers are in range 1-6
            valid_answers = [ans for ans in correct_ans.split(',') if ans in ['1','2','3','4','5','6']]
            if not valid_answers:
                valid_answers = [str(random.randint(1, 6))]  # Randomly assign a number if no valid answers
            row[7] = ','.join(valid_answers)
            
            writer.writerow(row)

# Usage
input_file = 'certshared.csv'
output_file = 'certshared_fixed.csv'
fix_csv(input_file, output_file)