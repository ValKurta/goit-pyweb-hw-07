from datetime import datetime
import faker
from random import randint, choice
import sqlite3

NUMBER_STUDENTS = 50
NUMBER_GROUPS = 3
NUMBER_SUBJECTS = 8
NUMBER_TEACHERS = 8
NUMBER_GRADES = 1000

def generate_fake_data():
    fake = faker.Faker()

    fake_groups = [fake.company()
                   for _ in range(NUMBER_GROUPS)]
    fake_teachers = [(fake.first_name(),
                      fake.last_name())
                     for _ in range(NUMBER_TEACHERS)]
    fake_subjects = [(fake.job(),
                      (i % NUMBER_TEACHERS) + 1)
                     for i in range(NUMBER_SUBJECTS)]

    fake_students = [(fake.first_name(),
                      fake.last_name(),
                      choice(range(1, NUMBER_GROUPS + 1)),
                      fake.date_of_birth())
                     for _ in range(NUMBER_STUDENTS)]

    return fake_groups, fake_teachers, fake_subjects, fake_students


def insert_data_to_db(groups, teachers, subjects, students):
    with sqlite3.connect('school.db') as con:
        cur = con.cursor()

        cur.executemany("INSERT INTO Groups (Group_Name) VALUES (?)", [(group,) for group in groups])
        print("INSERT INTO Groups (Group_Name) VALUES (?)", [(group,) for group in groups])
        cur.executemany("INSERT INTO Teachers (First_Name, Last_Name) VALUES (?, ?)", teachers)
        print("INSERT INTO Teachers (First_Name, Last_Name) VALUES (?, ?)", teachers)
        cur.executemany("INSERT INTO Subjects (Subject_Name, Teacher_ID) VALUES (?, ?)", subjects)
        print("INSERT INTO Subjects (Subject_Name, Teacher_ID) VALUES (?, ?)", subjects)
        cur.executemany("INSERT INTO Students (First_Name, Last_Name, Group_ID, Date_Of_Birth) VALUES (?, ?, ?, ?)",
                        students)
        print("INSERT INTO Students (First_Name, Last_Name, Group_ID, Date_Of_Birth) VALUES (?, ?, ?, ?)", students)

        cur.execute("SELECT Student_ID FROM Students")
        student_ids = [row[0] for row in cur.fetchall()]

        cur.execute("SELECT Subject_ID FROM Subjects")
        subject_ids = [row[0] for row in cur.fetchall()]

        fake = faker.Faker()
        fake_grades = [(choice(student_ids),
                        choice(subject_ids),
                        str(randint(2, 6)).zfill(2),
                        fake.date())
                       for _ in range(NUMBER_GRADES)]
        cur.executemany("INSERT INTO Grades (Student_ID, Subject_ID, Grade, Date_Received) VALUES (?, ?, ?, ?)",
                        fake_grades)

        print("INSERT INTO Grades (Student_ID, Subject_ID, Grade, Date_Received) VALUES (?, ?, ?, ?)", fake_grades)

        con.commit()


if __name__ == "__main__":
    groups, teachers, subjects, students = generate_fake_data()
    insert_data_to_db(groups, teachers, subjects, students)
