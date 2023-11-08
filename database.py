# Handles all database operations
# Connection object is passed in from main.py as to not create multiple connections
import sqlite3

# uses name of database to connect locally
def connect_db():
    return sqlite3.connect('StudentDB.db')

def close_connection(conn):
    conn.close()

def create_table(conn):
    with conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS Student(StudentId INTEGER PRIMARY KEY, FirstName TEXT,
        LastName TEXT, GPA REAL, Major TEXT, FacultyAdvisor TEXT, Address TEXT, City TEXT,
        State TEXT, ZipCode TEXT, MobilePhoneNumber TEXT, isDeleted INTEGER)""")
        print("Table created successfully.")

# Utilizes student data from csv_reader.py, uses named placeholders to insert data into the database
def insert_student(conn, student_data):
    sql_insert = """
    INSERT INTO Student (
        FirstName, LastName, GPA, Major, FacultyAdvisor,
        Address, City, State, ZipCode, MobilePhoneNumber, isDeleted
    ) VALUES (
        :FirstName, :LastName, :GPA, :Major, :FacultyAdvisor,
        :Address, :City, :State, :ZipCode, :MobilePhoneNumber, :isDeleted
    );
    """
    cursor = conn.cursor()
    cursor.execute(sql_insert, student_data)
    conn.commit()


def display_students(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Student WHERE isDeleted = 0")
    students = cursor.fetchall()

    print("\nAll Students and Their Attributes:")
    for student in students:
        print("StudentId:", student[0])
        print("First Name:", student[1])
        print("Last Name:", student[2])
        print("GPA:", student[3])
        print("Major:", student[4])
        print("Faculty Advisor:", student[5])
        print("Address:", student[6])
        print("City:", student[7])
        print("State:", student[8])
        print("Zip Code:", student[9])
        print("Mobile Phone Number:", student[10])
        print("-------------------------------")




# Uses passed parameters to insert data into the database
def db_add_student(conn, first_name, last_name, gpa, major, advisor, mobile_phone, address, city, state, zip_code):
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO Student (FirstName, LastName, GPA, Major, FacultyAdvisor, MobilePhoneNumber,
         Address, City, State, ZipCode, isDeleted) VALUES (?,?,?,?,?,?,?,?,?,?,0)""",
        (first_name, last_name, gpa, major, advisor, mobile_phone, address, city, state, zip_code))
    conn.commit()


def get_max_student_id(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(StudentId) FROM Student")
    return cursor.fetchone()[0]


def get_student_by_id(conn, student_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Student WHERE StudentId=?", (student_id,))
    return cursor.fetchone()


# finds the current fields for the student and then updates the fields that are not None
def db_update_student(conn, student_id, new_major, new_advisor, new_mobile_phone):
    student = list(get_student_by_id(conn, student_id))  
    print(student[10])
    if new_major is None:
        new_major = student[4] #If no new major was provided, use the old one
    if new_advisor is None:
        new_advisor = student[5]
    if new_mobile_phone is None:
        new_mobile_phone = student[10]
    cursor = conn.cursor()
    cursor.execute("UPDATE Student SET Major=?, FacultyAdvisor=?, MobilePhoneNumber=? WHERE StudentId=?",
                   (new_major, new_advisor, new_mobile_phone, student_id))
    conn.commit()

# Soft deletes by setting isDeleted to 1
def db_delete_student(conn, student_id):
    cursor = conn.cursor()
    cursor.execute("UPDATE Student SET isDeleted=1 WHERE StudentId=?", (student_id,))
    print("Student deleted successfully!")
    conn.commit()


def search_by_major(conn, major):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Student WHERE Major=?", (major,))
    rows = cursor.fetchall()
    for row in rows:
        print(f"""Student ID: {row[0]}, Name: {row[1]}{row[2]}, Major: {row[4]}, Advisor: {row[5]}, Mobile Phone:
         {row[10]}""")


def search_by_city(conn, city):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Student WHERE City=?", (city,))
    rows = cursor.fetchall()
    for row in rows:
        print(f"""Student ID: {row[0]}, Name: {row[1]}{row[2]}, Major: {row[4]}, Advisor: {row[5]}, Mobile Phone:
         {row[10]}""")


def search_by_state(conn, state):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Student WHERE State=?", (state,))
    rows = cursor.fetchall()
    for row in rows:
        print(f"""Student ID: {row[0]}, Name: {row[1]}{row[2]}, Major: {row[4]}, Advisor: {row[5]}, Mobile Phone:
         {row[10]}""")


def search_by_advisor(conn, advisor):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Student WHERE FacultyAdvisor=?", (advisor,))
    rows = cursor.fetchall()
    for row in rows:
        print(f"""Student ID: {row[0]}, Name: {row[1]}{row[2]}, Major: {row[4]}, Advisor: {row[5]}, Mobile Phone:
         {row[10]}""")


def search_by_gpa(conn, gpa):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Student WHERE GPA=?", (gpa,))
    rows = cursor.fetchall()
    for row in rows:
        print(f"""Student ID: {row[0]}, Name: {row[1]}{row[2]}, Major: {row[4]}, Advisor: {row[5]}, Mobile Phone:
        {row[10]}""")
