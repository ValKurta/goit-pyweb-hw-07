from datetime import datetime
import faker
from random import randint, choice
from sqlalchemy.orm import Session
from database import engine, get_session, Base
from models import Groups, Teachers, Subjects, Students, Grades

NUMBER_STUDENTS = 50
NUMBER_GROUPS = 3
NUMBER_SUBJECTS = 8
NUMBER_TEACHERS = 8
NUMBER_GRADES = 1000


def generate_fake_data():
    fake = faker.Faker()

    fake_groups = [Groups(Group_Name=fake.company())
                   for _ in range(NUMBER_GROUPS)]
    fake_teachers = [Teachers(First_Name=fake.first_name(),
                              Last_Name=fake.last_name())
                     for _ in range(NUMBER_TEACHERS)]
    fake_subjects = [Subjects(Subject_Name=fake.job(),
                              Teacher_ID=(i % NUMBER_TEACHERS) + 1)
                     for i in range(NUMBER_SUBJECTS)]
    fake_students = [Students(First_Name=fake.first_name(),
                              Last_Name=fake.last_name(),
                              Group_ID=choice(range(1, NUMBER_GROUPS + 1)),
                              Date_Of_Birth=fake.date_of_birth())
                     for _ in range(NUMBER_STUDENTS)]

    return fake_groups, fake_teachers, fake_subjects, fake_students


def insert_data_to_db(groups, teachers, subjects, students):
    session = get_session()
    try:
        session.add_all(groups)
        session.add_all(teachers)
        session.add_all(subjects)
        session.add_all(students)
        session.commit()

        student_ids = [student.Student_ID for student in session.query(Students.Student_ID).all()]
        subject_ids = [subject.Subject_ID for subject in session.query(Subjects.Subject_ID).all()]

        fake = faker.Faker()
        fake_grades = [Grades(Student_ID=choice(student_ids),
                              Subject_ID=choice(subject_ids),
                              Grade=randint(2, 6),
                              Date_Received=fake.date())
                       for _ in range(NUMBER_GRADES)]
        session.add_all(fake_grades)
        session.commit()

        print("Data inserted successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
        session.rollback()
    finally:
        session.close()


if __name__ == "__main__":
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    groups, teachers, subjects, students = generate_fake_data()
    insert_data_to_db(groups, teachers, subjects, students)
