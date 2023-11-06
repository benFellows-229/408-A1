from csv_reader import *
from database import *
from ui import *

def main():
    conn = connect_db()
    create_table(conn)

    students = read_students_from_csv('students.csv')
    for student_data in students:
        insert_student(conn, student_data)  # student_data is passed to the insert function

    close_connection(conn)
    ui()

if __name__ == "__main__":
    main()
