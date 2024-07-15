DROP TABLE IF EXISTS Students;
CREATE TABLE Students (
    Student_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    First_Name TEXT,
    Last_Name TEXT,
    Group_ID INTEGER,
    Date_Of_Birth DATE,
    FOREIGN KEY (Group_ID) REFERENCES Groups(Group_ID)
);

DROP TABLE IF EXISTS Groups;
CREATE TABLE Groups (
    Group_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Group_Name TEXT
);

DROP TABLE IF EXISTS Teachers;
CREATE TABLE Teachers (
    Teacher_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    First_Name TEXT,
    Last_Name TEXT
);

DROP TABLE IF EXISTS Subjects;
CREATE TABLE Subjects (
    Subject_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Subject_Name TEXT,
    Teacher_ID INTEGER,
    FOREIGN KEY (Teacher_ID) REFERENCES Teachers(Teacher_ID)
);

DROP TABLE IF EXISTS Grades;
CREATE TABLE Grades (
    Grade_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Student_ID INTEGER,
    Subject_ID INTEGER,
    Grade TEXT CHECK(LENGTH(Grade) > 1 AND LENGTH(Grade) < 7),
    Date_Received DATE,
    FOREIGN KEY (Student_ID) REFERENCES Students(Student_ID),
    FOREIGN KEY (Subject_ID) REFERENCES Subjects(Subject_ID)
);
