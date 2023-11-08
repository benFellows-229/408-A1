from csv_reader import read_students_from_csv
from database import create_table, connect_db, close_connection, insert_student
from ui import ui

# Uses all the functions from the other files to create the database and run the program,
# conn object is passed into various functions to avoid creating multiple connections
def main():
    conn = connect_db()
    create_table(conn)

    # Read students from CSV and insert into database
    students = read_students_from_csv('students.csv')
    for student_data in students:
        insert_student(conn, student_data)  

    ui(conn)
    close_connection(conn)


if __name__ == "__main__":
    main()
