import asyncio
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, delete
from models import Grades
from database import get_async_session


async def create_grade(session: AsyncSession, student_id: int, subject_id: int, grade: int, date_received: str):
    grade_entry = Grades(Student_ID=student_id, Subject_ID=subject_id, Grade=grade, Date_Received=date_received)
    session.add(grade_entry)
    await session.commit()
    print(f"Grade for student ID {student_id} in subject ID {subject_id} created.")


async def list_grades(session: AsyncSession):
    result = await session.execute(select(Grades))
    grades = result.scalars().all()
    for grade in grades:
        print(f"ID: {grade.Grade_ID}, "
              f"Student ID: {grade.Student_ID}, "
              f"Subject ID: {grade.Subject_ID}, "
              f"Grade: {grade.Grade}, "
              f"Date Received: {grade.Date_Received}")


async def update_grade(session: AsyncSession, grade_id: int, student_id: int, subject_id: int, grade: int, date_received: str):
    await session.execute(
        update(Grades)
        .where(Grades.Grade_ID == grade_id)
        .values(Student_ID=student_id, Subject_ID=subject_id, Grade=grade, Date_Received=date_received)
    )
    await session.commit()
    print(f"Grade with ID {grade_id} updated.")


async def delete_grade(session: AsyncSession, grade_id: int):
    await session.execute(delete(Grades).where(Grades.Grade_ID == grade_id))
    await session.commit()
    print(f"Grade with ID {grade_id} deleted.")


async def grade_operations(args):
    async with get_async_session() as session:
        if args.action == 'create':
            await create_grade(session, args.student_id, args.subject_id, args.grade, args.date_received)
        elif args.action == 'list':
            await list_grades(session)
        elif args.action == 'update':
            await update_grade(session, args.id, args.student_id, args.subject_id, args.grade, args.date_received)
        elif args.action == 'remove':
            await delete_grade(session, args.id)
