# Serves as a basic TUI for the database
from database import (db_add_student, get_max_student_id, db_update_student, db_delete_student, search_by_major,
                      search_by_gpa, search_by_city, search_by_state, search_by_advisor, display_students)


def ui(conn):
    selection = ''
    while selection != '6':
        selection = input("""\nWhat would you like to do?
1. Display all students
2. Add a student
3. Update a student
4. Delete a student
5. Search for a student
6. Exit\n""")
        if selection == '0':
            return
        elif selection == '1':
            display_students(conn)
        elif selection == '2':
            add_student(conn)
        elif selection == '3':
            update_student(conn)
        elif selection == '4':
            delete_student(conn)
        elif selection == '5':
            search_students(conn)

# Parses input until user enters a name containing characters commonly found in names/places
def validate_name(name):
    while True:
        try:
            name = str(name)
            if all(char.isalpha() or char in '- ' for char in name):
                return name
            else:
                name = input("Invalid input. Please enter a valid string:\n")
        except ValueError:
            name = input("Invalid input. Please enter a valid string:\n")

# Parses input until user enters a valid zip code
def validate_zip_code(zip_code):
    while True:
        try:
            zip_code = int(zip_code)
            if len(str(zip_code)) == 5:
                return zip_code
            else:
                zip_code = input("Invalid Zip Code. Please enter a valid zip code:\n")
        except ValueError:
            zip_code = input("Invalid Zip Code. Please enter a valid zip code:\n")

# Uses list of states to validate input
def validate_state(state):
    states = ['al', 'ak', 'az', 'ar', 'ca', 'co', 'ct', 'de', 'fl', 'ga', 'hi', 'id', 'il', 'in', 'ia', 'ks', 
              'ky', 'la', 'me', 'md', 'ma', 'mi', 'mn', 'ms', 'mo', 'mt', 'ne', 'nv', 'nh', 'nj', 'nm', 'ny', 
              'nc', 'nd', 'oh', 'ok', 'or', 'pa', 'ri', 'sc', 'sd', 'tn', 'tx', 'ut', 'vt', 'va', 'wa', 'wv', 
              'wi', 'wy', 'alabama', 'alaska', 'arizona', 'arkansas', 'california', 'colorado', 'connecticut', 
              'delaware', 'florida', 'georgia', 'hawaii', 'idaho', 'illinois', 'indiana', 'iowa', 'kansas', 
              'kentucky', 'louisiana', 'maine', 'maryland', 'massachusetts', 'michigan', 'minnesota', 'mississippi', 
              'missouri', 'montana', 'nebraska', 'nevada', 'new hampshire', 'new jersey', 'new mexico', 'new york', 
              'north carolina', 'north dakota', 'ohio', 'oklahoma', 'oregon', 'pennsylvania', 'rhode island', 
              'south carolina', 'south dakota', 'tennessee', 'texas', 'utah', 'vermont', 'virginia', 'washington', 
              'west virginia', 'wisconsin', 'wyoming']
    while True:
        try:
            state = str(state)
            if state.lower() in states:
                return state
            else:
                state = input("Invalid State. Please enter a valid state:\n")
        except ValueError:
            state = input("Invalid State. Please enter a valid state:\n")

# Only allows for numbers and common phone number characters
def validate_phone_number(phone_number):
    while True:
        if all(char.isdigit() or char in '()-x. ' for char in phone_number):
            return phone_number
        else:
            phone_number = input("Invalid Phone Number. Please enter a valid phone number:\n")

# Only allows for floats within 0 and the max range of weighted GPAs 4.8
def validate_gpa(gpa):
    while True:
        try:
            gpa = float(gpa)
            if 0.0 <= gpa <= 4.8:
                return gpa
            else:
                gpa = input("Invalid GPA. Please enter a valid GPA:\n")
        except ValueError:
            gpa = input("Invalid GPA. Please enter a valid GPA:\n")

# Parses input until user enters a valid student ID
def validate_student_id(conn, student_id):
    while True:
        try:
            student_id = int(student_id)
            max_student_id = get_max_student_id(conn) 
            if student_id > max_student_id: # Checks that the student ID is not greater than the highest current ID
                student_id = input("Invalid Student ID. Please enter a valid student ID:\n")
            else:
                return student_id
        except ValueError:
            student_id = input("Invalid Student ID. Please enter a valid student ID:\n")

# Prompts user for student data and validates inputs before adding to database
def add_student(conn):
    print("Enter student details:")
    first_name = validate_name(input("First Name: "))
    last_name = validate_name(input("Last Name: "))
    gpa = validate_gpa(input("GPA: "))
    major = validate_name(input("Major: "))
    advisor = validate_name(input("Faculty Advisor: "))
    address = input("Address: ") # Address is not validated because it can contain numbers and other characters
    city = validate_name(input("City: "))
    state = validate_state(input("State: "))
    zip_code = validate_zip_code(input("Zip Code: "))
    mobile_phone = validate_phone_number(input("Mobile Phone Number: "))
    db_add_student(conn, first_name, last_name, gpa, major, advisor, mobile_phone, address, city, state, zip_code)
    conn.commit()
    print("Student added successfully!")

# Checks which fields the user would like to update and validates inputs before updating database based on student ID
def update_student(conn):
    new_advisor = None
    new_major = None
    new_mobile_phone = None
    print("Enter the ID of the student you would like to update:")
    student_id = validate_student_id(conn, input("Student ID: "))

    in_major = input("Would you like to update the Major field? (y/n): ")
    if in_major.lower() == 'y':
        new_major = validate_name(input("Major: "))
    in_advisor = input("Would you like to update the Advisor field? (y/n): ")
    if in_advisor.lower() == 'y':
        new_advisor = validate_name(input("Faculty Advisor: "))
    in_phone = input("Would you like to update the Mobile Phone Number field? (y/n): ")
    if in_phone.lower() == 'y':
        new_mobile_phone = validate_phone_number(input("Mobile Phone Number: "))
        # Update the student in the database
    db_update_student(conn, student_id, new_major, new_advisor, new_mobile_phone)
    conn.commit()
    print("Student updated successfully!")

# Validates student ID before soft deleting student from database
def delete_student(conn):
    s_id = validate_student_id(conn, input("Enter the ID of the student you would like to delete:"))
    db_delete_student(conn, s_id)

# Checks which field the user would like to search by and validates inputs before searching database
def search_students(conn):
    select = input("""Which field would you like to search by?
1. Major
2. GPA
3. City
4. State
5. Advisor
""")
    if select == '1':
        in_major = validate_name(input("Major: "))
        search_by_major(conn, in_major)
    elif select == '2':
        in_gpa = validate_gpa(input("GPA: "))
        search_by_gpa(conn, in_gpa)
    elif select == '3':
        in_city = validate_name(input("City: "))
        search_by_city(conn, in_city)
    elif select == '4':
        in_state = validate_state(input("State: "))
        search_by_state(conn, in_state)
    elif select == '5':
        in_advisor = validate_name(input("Advisor: "))
        search_by_advisor(conn, in_advisor)
    else:
        print("Invalid input. Please enter a valid input.")
        search_students(conn)
