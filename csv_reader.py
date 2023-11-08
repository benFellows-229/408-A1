import csv
import itertools

# Reads student data from a CSV file and yields a dictionary of the student data
def read_students_from_csv(csv_filename):
    advisors = ['Dr. Smith', 'Dr. Jones', 'Dr. Williams', 'Dr. Brown', 'Dr. Miller', 'Dr. Davis', 'Dr. Garcia',]
    advisor_cycle = itertools.cycle(advisors) # Cycle through the list of advisors
    
    with open(csv_filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            yield { # Yield a dictionary of the student data
                'FirstName': row['FirstName'],
                'LastName': row['LastName'],
                'GPA': row['GPA'],
                'Major': row['Major'],
                'FacultyAdvisor': next(advisor_cycle), 
                'Address': row['Address'],
                'City': row['City'],
                'State': row['State'],
                'ZipCode': row['ZipCode'],
                'MobilePhoneNumber': row['MobilePhoneNumber'],
                'isDeleted': 0  # Assuming new entries are not deleted
            }
