import csv


def read_students_from_csv(csv_filename):
    with open(csv_filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            yield {
                'FirstName': row['FirstName'],
                'LastName': row['LastName'],
                'GPA': row['GPA'],
                'Major': row['Major'],
                'FacultyAdvisor': row.get('FacultyAdvisor', None),  # Assuming the field can be None
                'Address': row['Address'],
                'City': row['City'],
                'State': row['State'],
                'ZipCode': row['ZipCode'],
                'MobilePhoneNumber': row['MobilePhoneNumber'],
                'isDeleted': 0  # Assuming new entries are not deleted
            }
