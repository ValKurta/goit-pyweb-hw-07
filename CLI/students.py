import asyncio
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, delete
from models import Students
from database import get_async_session


async def create_student(session: AsyncSession, first_name: str, last_name: str, date_of_birth: str, group_id: int):
    student = Students(First_Name=first_name, Last_Name=last_name, Date_Of_Birth=date_of_birth, Group_ID=group_id)
    session.add(student)
    await session.commit()
    print(f"Student {first_name} {last_name} created.")


async def list_students(session: AsyncSession):
    result = await session.execute(select(Students))
    students = result.scalars().all()
    for student in students:
        print(f"ID: {student.Student_ID}, Name: {student.First_Name} {student.Last_Name}, Date of Birth: {student.Date_Of_Birth}, Group ID: {student.Group_ID}")


async def update_student(session: AsyncSession, student_id: int, first_name: str, last_name: str, date_of_birth: str, group_id: int):
    await session.execute(
        update(Students)
        .where(Students.Student_ID == student_id)
        .values(First_Name=first_name, Last_Name=last_name, Date_Of_Birth=date_of_birth, Group_ID=group_id)
    )
    await session.commit()
    print(f"Student with ID {student_id} updated.")


async def delete_student(session: AsyncSession, student_id: int):
    await session.execute(delete(Students).where(Students.Student_ID == student_id))
    await session.commit()
    print(f"Student with ID {student_id} deleted.")


async def student_operations(args):
    async with get_async_session() as session:
        if args.action == 'create':
            await create_student(session, args.first_name, args.last_name, args.date_of_birth, args.group_id)
        elif args.action == 'list':
            await list_students(session)
        elif args.action == 'update':
            await update_student(session, args.id, args.first_name, args.last_name, args.date_of_birth, args.group_id)
        elif args.action == 'remove':
            await delete_student(session, args.id)
