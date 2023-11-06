import sqlite3


def connect_db():
    return sqlite3.connect('StudentDB.db')


def create_table(conn):
    with conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS Student(StudentId INTEGER PRIMARY KEY, FirstName TEXT,
        LastName TEXT, GPA REAL, Major TEXT, FacultyAdvisor TEXT, Address TEXT, City TEXT,
        State TEXT, ZipCode TEXT, MobilePhoneNumber TEXT, isDeleted INTEGER)""")
        print("Table created successfully.")


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


def close_connection(conn):
    conn.close()
