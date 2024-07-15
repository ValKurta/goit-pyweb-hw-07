from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, CheckConstraint
from sqlalchemy.orm import relationship
from database import Base

class Groups(Base):
    __tablename__ = 'Groups'
    Group_ID = Column(Integer, primary_key=True, autoincrement=True)
    Group_Name = Column(String(250), nullable=False)

    students = relationship("Students", back_populates="group")

class Teachers(Base):
    __tablename__ = 'Teachers'
    Teacher_ID = Column(Integer, primary_key=True, autoincrement=True)
    First_Name = Column(String(250), nullable=False)
    Last_Name = Column(String(250), nullable=False)

    subjects = relationship("Subjects", back_populates="teacher")

class Subjects(Base):
    __tablename__ = 'Subjects'
    Subject_ID = Column(Integer, primary_key=True, autoincrement=True)
    Subject_Name = Column(String(250), nullable=False)
    Teacher_ID = Column(Integer, ForeignKey('Teachers.Teacher_ID'), nullable=False)

    teacher = relationship("Teachers", back_populates="subjects")
    grades = relationship("Grades", back_populates="subject")

class Students(Base):
    __tablename__ = 'Students'
    Student_ID = Column(Integer, primary_key=True, autoincrement=True)
    First_Name = Column(String(250), nullable=False)
    Last_Name = Column(String(250), nullable=False)
    Date_Of_Birth = Column(Date, nullable=False)
    Group_ID = Column(Integer, ForeignKey('Groups.Group_ID'), nullable=False)

    group = relationship("Groups", back_populates="students")
    grades = relationship("Grades", back_populates="student")

class Grades(Base):
    __tablename__ = 'Grades'
    Grade_ID = Column(Integer, primary_key=True, autoincrement=True)
    Student_ID = Column(Integer, ForeignKey('Students.Student_ID'), nullable=False)
    Subject_ID = Column(Integer, ForeignKey('Subjects.Subject_ID'), nullable=False)
    Date_Received = Column(DateTime, nullable=False)
    Grade = Column(Integer, nullable=False)

    __table_args__ = (
        CheckConstraint('"Grade" > 1 AND "Grade" < 7', name='check_grade_between_1_and_7'),
    )

    student = relationship("Students", back_populates="grades")
    subject = relationship("Subjects", back_populates="grades")
