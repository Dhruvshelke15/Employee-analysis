import csv
from datetime import datetime, timedelta

# Reading the file
with open('assignment.csv', 'r') as file:
    reader = csv.DictReader(file)
    data = list(reader)

# Checking the entries
for entry in data:
    if entry['Time'] != '':
        entry['Time'] = datetime.strptime(entry['Time'], '%m/%d/%Y %I:%M %p')
    if entry['Time Out'] != '':
        entry['Time Out'] = datetime.strptime(entry['Time Out'], '%m/%d/%Y %I:%M %p')

# Sorting data by Employee Name and then by Time
data.sort(key=lambda x: (x['Employee Name'], x['Time']))

# Track consecutive days and shift hours
consecutive_days = {}
shift_hours = {}
consecutive_days_threshold = 7
min_shift_interval = timedelta(hours=1)
max_shift_hours = timedelta(hours=14)

# Store results in a list
results = []

# Process the data
for entry in data:
    name = entry['Employee Name']
    if name not in consecutive_days:
        consecutive_days[name] = set()
        shift_hours[name] = timedelta()
    
    # Check for consecutive days worked
    if entry['Time'] != '':
        consecutive_days[name].add(entry['Time'].date())
        if len(consecutive_days[name]) >= consecutive_days_threshold:
            result = f"{name} has worked for {len(consecutive_days[name])} consecutive days."
            results.append(result)

    # Calculate shift duration
    if entry['Time'] != '' and entry['Time Out'] != '':
        shift_duration = entry['Time Out'] - entry['Time']
        shift_hours[name] += shift_duration

    # Check for short shift intervals
    if entry['Time'] != '' and entry['Time Out'] != '' and shift_duration < min_shift_interval:
        result = f"{name} has less than 10 hours between shifts on {entry['Time'].date()}."
        results.append(result)

    # Check for long shifts
    if shift_hours[name] > max_shift_hours:
        result = f"{name} has worked for more than 14 hours on {entry['Time'].date()}."
        results.append(result)

# Write results to a CSV file
with open('results.csv', 'w', newline='') as result_file:
    writer = csv.writer(result_file)
    writer.writerow(['Result'])
    writer.writerows([[result] for result in results])
