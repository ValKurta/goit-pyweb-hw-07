import asyncio
from sqlalchemy import select, func, cast, Integer, text
from models import Students, Grades, Subjects, Groups, Teachers
from database import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession

async def select_1(session: AsyncSession):
    subquery = (
        select(
            Grades.Student_ID,
            func.avg(cast(Grades.Grade, Integer)).label('average_grade')
        )
        .group_by(Grades.Student_ID)
        .subquery()
    )

    results = (
        await session.execute(
            select(
                Students.Student_ID,
                Students.First_Name,
                Students.Last_Name,
                Students.Group_ID,
                Students.Date_Of_Birth,
                subquery.c.average_grade.label('Grade')
            )
            .join(subquery, Students.Student_ID == subquery.c.Student_ID)
            .order_by(subquery.c.average_grade.desc())
            .limit(5)
        )
    )

    return results.fetchall()


async def select_2(session: AsyncSession):
    subquery_a = (
        select(
            Grades.Student_ID,
            Grades.Subject_ID,
            func.avg(cast(Grades.Grade, Integer)).label('Average_Grade')
        )
        .group_by(Grades.Student_ID, Grades.Subject_ID)
        .subquery()
    )

    subquery_b = (
        select(
            subquery_a.c.Student_ID,
            subquery_a.c.Subject_ID,
            subquery_a.c.Average_Grade,
            func.dense_rank().over(
                partition_by=subquery_a.c.Subject_ID,
                order_by=subquery_a.c.Average_Grade.desc()
            ).label('rn')
        )
        .subquery()
    )

    results = (
        await session.execute(
            select(
                Subjects.Subject_Name,
                subquery_b.c.Average_Grade,
                Students.First_Name,
                Students.Last_Name,
                Groups.Group_Name
            )
            .join(Students, Students.Student_ID == subquery_b.c.Student_ID)
            .join(Subjects, Subjects.Subject_ID == subquery_b.c.Subject_ID)
            .join(Groups, Groups.Group_ID == Students.Group_ID)
            .filter(subquery_b.c.rn == 1)
        )
    )

    return results.fetchall()


async def select_3(session: AsyncSession):
    results = (
        await session.execute(
            select(
                Groups.Group_Name,
                Subjects.Subject_Name,
                (cast(func.avg(cast(Grades.Grade, Integer)) * 10, Integer) / 10.0).label('AverageGrade')
            )
            .join(Students, Grades.Student_ID == Students.Student_ID)
            .join(Groups, Students.Group_ID == Groups.Group_ID)
            .join(Subjects, Grades.Subject_ID == Subjects.Subject_ID)
            .group_by(Groups.Group_Name, Subjects.Subject_Name)
            .order_by(Groups.Group_Name, Subjects.Subject_Name)
        )
    )

    return results.fetchall()


async def select_4(session: AsyncSession):
    result = (
        await session.execute(
            select(func.avg(cast(Grades.Grade, Integer)).label('AverageGrade'))
        )
    )

    return result.scalar_one()


async def select_5(session: AsyncSession):
    results = (
        await session.execute(
            select(
                Teachers.First_Name,
                Teachers.Last_Name,
                Subjects.Subject_Name
            )
            .join(Teachers, Subjects.Teacher_ID == Teachers.Teacher_ID)
        )
    )

    return results.fetchall()


async def select_6(session: AsyncSession):
    results = (
        await session.execute(
            select(
                Groups.Group_Name,
                Students
            )
            .join(Students, Groups.Group_ID == Students.Group_ID)
            .where(Groups.Group_Name == "Young-Hardin")
            .order_by(Students.Last_Name)
        )
    )

    return results.fetchall()


async def select_7(session: AsyncSession):
    group_name_subquery = select(Groups.Group_Name).limit(1).scalar_subquery()
    subject_name_subquery = select(Subjects.Subject_Name).limit(1).scalar_subquery()

    results = (
        await session.execute(
            select(
                Groups.Group_Name,
                Subjects.Subject_Name,
                (Students.First_Name + ' ' + Students.Last_Name).label('Full_Name'),
                cast(Grades.Grade, Integer).label('Grade')
            )
            .join(Students, Students.Student_ID == Grades.Student_ID)
            .join(Groups, Groups.Group_ID == Students.Group_ID)
            .join(Subjects, Subjects.Subject_ID == Grades.Subject_ID)
            .where(
                Groups.Group_Name == group_name_subquery,
                Subjects.Subject_Name == subject_name_subquery
            )
            .order_by(Students.Last_Name)
        )
    )

    return results.fetchall()


async def select_8(session: AsyncSession):
    results = (
        await session.execute(
            select(
                Teachers.First_Name,
                Teachers.Last_Name,
                func.avg(cast(Grades.Grade, Integer)).label('AverageGrade')
            )
            .join(Subjects, Subjects.Teacher_ID == Teachers.Teacher_ID)
            .outerjoin(Grades, Grades.Subject_ID == Subjects.Subject_ID)
            .group_by(Teachers.First_Name, Teachers.Last_Name)
            .order_by(func.avg(cast(Grades.Grade, Integer)).desc())
        )
    )

    return results.fetchall()


async def select_9(session: AsyncSession):
    latest_student_id_subquery = select(Students.Student_ID).order_by(Students.Student_ID.desc()).limit(1).scalar_subquery()

    results = (
        await session.execute(
            select(
                Subjects.Subject_Name
            )
            .distinct()
            .join(Grades, Grades.Subject_ID == Subjects.Subject_ID)
            .join(Students, Students.Student_ID == Grades.Student_ID)
            .where(Grades.Student_ID == latest_student_id_subquery)
            .order_by(Subjects.Subject_Name)
        )
    )

    return results.fetchall()


async def select_10(session: AsyncSession):
    results = (
        await session.execute(
            select(
                Subjects.Subject_Name
            )
            .distinct()
            .join(Grades, Grades.Subject_ID == Subjects.Subject_ID)
            .join(Students, Students.Student_ID == Grades.Student_ID)
            .join(Teachers, Teachers.Teacher_ID == Subjects.Teacher_ID)
            .where(
                (Students.First_Name + ' ' + Students.Last_Name) == 'Katherine Moore',
                (Teachers.First_Name + ' ' + Teachers.Last_Name) == 'Rebekah Cross'
            )
            .order_by(Subjects.Subject_Name)
        )
    )

    return results.fetchall()


async def select_11(session: AsyncSession):
    results = (
        await session.execute(
            select(
                (Teachers.First_Name + ' ' + Teachers.Last_Name).label('Teacher_Full_Name'),
                (Students.First_Name + ' ' + Students.Last_Name).label('Student_Full_Name'),
                (cast(func.avg(cast(Grades.Grade, Integer)) * 10, Integer) / 10.0).label('AverageGrade')
            )
            .join(Subjects, Subjects.Teacher_ID == Teachers.Teacher_ID)
            .join(Grades, Grades.Subject_ID == Subjects.Subject_ID)
            .join(Students, Students.Student_ID == Grades.Student_ID)
            .group_by(Teachers.First_Name, Teachers.Last_Name, Students.First_Name, Students.Last_Name)
            .order_by(Teachers.Last_Name, Teachers.First_Name, func.avg(cast(Grades.Grade, Integer)).desc())
        )
    )

    return results.fetchall()


async def select_12(session: AsyncSession):
    subquery_grades = (
        select(
            Grades,
            func.row_number().over(
                partition_by=[Grades.Student_ID, Grades.Subject_ID],
                order_by=Grades.Date_Received.desc()
            ).label('rn')
        ).alias('a')
    )

    group_id_subquery = select(Groups.Group_ID).limit(1).scalar_subquery()
    subject_id_subquery = select(Subjects.Subject_ID).limit(1).scalar_subquery()

    results = (
        await session.execute(
            select(
                Groups.Group_Name,
                Subjects.Subject_Name,
                Students.First_Name,
                Students.Last_Name,
                subquery_grades.c.Date_Received
            )
            .join(Students, Students.Student_ID == subquery_grades.c.Student_ID)
            .join(Groups, Groups.Group_ID == Students.Group_ID)
            .join(Subjects, Subjects.Subject_ID == subquery_grades.c.Subject_ID)
            .where(
                subquery_grades.c.rn == 1,
                Groups.Group_ID == group_id_subquery,
                subquery_grades.c.Subject_ID == subject_id_subquery
            )
        )
    )

    return results.fetchall()


async def main():
    async with AsyncSessionLocal() as session:

        s1 = await select_1(session)
        print(f"\nЗнайти 5 студентів із найбільшим середнім балом з усіх предметів:\n")
        for record in s1:
            print(f"ID: {record.Student_ID}, "
                  f"Name: {record.First_Name} {record.Last_Name}, "
                  f"Average Grade: {record.Grade}")
        print(f"\n---\n")

        s2 = await select_2(session)
        print(f"\nЗнайти студента із найвищим середнім балом з певного предмета:\n")
        for record in s2:
            print(f"Subject: {record.Subject_Name}, "
                  f"Average Grade: {record.Average_Grade}, "
                  f"Name: {record.First_Name} {record.Last_Name}, "
                  f"Group: {record.Group_Name}")
        print(f"\n---\n")

        s3 = await select_3(session)
        print(f"\nЗнайти середній бал у групах з певного предмета:\n")
        for record in s3:
            print(f"Group: {record.Group_Name}, "
                  f"Subject: {record.Subject_Name}, "
                  f"Average Grade: {record.AverageGrade}")
        print(f"\n---\n")

        s4 = await select_4(session)
        print(f"\nЗнайти середній бал у групах з певного предмета:\nAverageGrade: {s4}")
        print(f"\n---\n")

        s5 = await select_5(session)
        print(f"\nЗнайти які курси читає певний викладач:\n")
        for record in s5:
            print(f"First Name: {record.First_Name}, ",
                  f"Last Name: {record.Last_Name}, ",
                  f"Subject Name: {record.Subject_Name}")
        print(f"\n---\n")

        s6 = await select_6(session)
        print(f"\nЗнайти список студентів у певній групі:\n")
        for record in s6:
            print(f"Group: {record.Group_Name}, "
                  f"ID: {record.Students.Student_ID}, "
                  f"Name: {record.Students.First_Name} {record.Students.Last_Name}, "
                  f"Group ID: {record.Students.Group_ID}, "
                  f"Date of Birth: {record.Students.Date_Of_Birth}")
        print(f"\n---\n")

        s7 = await select_7(session)
        print(f"\nЗнайти оцінки студентів у окремій групі з певного предмета:\n")
        for record in s7:
            print(f"Group: {record.Group_Name}, "
                  f"Subject: {record.Subject_Name}, "
                  f"Full Name: {record.Full_Name}, "
                  f"Grade: {record.Grade}")
        print(f"\n---\n")

        s8 = await select_8(session)
        print(f"\nЗнайти середній бал, який ставить певний викладач зі своїх предметів:\n")
        for record in s8:
            print(f"First Name: {record.First_Name}, "
                  f"Last Name: {record.Last_Name}, "
                  f"Average Grade: {record.AverageGrade}")
        print(f"\n---\n")

        s9 = await select_9(session)
        print(f"\nЗнайти список курсів, які відвідує студент:\n")
        for record in s9:
            print(f"Subject Name: {record.Subject_Name}")
        print(f"\n---\n")

        s10 = await select_10(session)
        print(f"\nСписок курсів, які певному студенту читає певний викладач:\n")
        for record in s10:
            print(f"Subject Name: {record.Subject_Name}")
        print(f"\n---\n")

        s11 = await select_11(session)
        print(f"\nСередній бал, який певний викладач ставить певному студентові:\n")
        for record in s11:
            print(f"Teacher Full Name: {record.Teacher_Full_Name}, "
                  f"Student Full Name: {record.Student_Full_Name}, "
                  f"Average Grade: {record.AverageGrade}")
        print(f"\n---\n")

        s12 = await select_12(session)
        print(f"\nОцінки студентів у певній групі з певного предмета на останньому занятті:\n")
        for record in s12:
            print(f"Group Name: {record.Group_Name}, "
                  f"Subject Name: {record.Subject_Name}, "
                  f"Student Full Name: {record.First_Name} {record.Last_Name}, "
                  f"Date Received: {record.Date_Received}")
        print(f"\n---\n")


if __name__ == "__main__":
    asyncio.run(main())
