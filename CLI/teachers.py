from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, delete
from models import Teachers
from database import get_async_session


async def create_teacher(session: AsyncSession, first_name: str, last_name: str):
    teacher = Teachers(First_Name=first_name, Last_Name=last_name)
    session.add(teacher)
    await session.commit()
    print(f"Teacher {first_name} {last_name} created.")


async def list_teachers(session: AsyncSession):
    result = await session.execute(select(Teachers))
    teachers = result.scalars().all()
    for teacher in teachers:
        print(f"ID: {teacher.Teacher_ID}, Name: {teacher.First_Name} {teacher.Last_Name}")


async def update_teacher(session: AsyncSession, teacher_id: int, first_name: str, last_name: str):
    await session.execute(
        update(Teachers)
        .where(Teachers.Teacher_ID == teacher_id)
        .values(First_Name=first_name, Last_Name=last_name)
    )
    await session.commit()
    print(f"Teacher with ID {teacher_id} updated.")


async def delete_teacher(session: AsyncSession, teacher_id: int):
    await session.execute(delete(Teachers).where(Teachers.Teacher_ID == teacher_id))
    await session.commit()
    print(f"Teacher with ID {teacher_id} deleted.")


async def teacher_operations(args):
    async for session in get_async_session():
        if args.action == 'create':
            await create_teacher(session, args.first_name, args.last_name)
        elif args.action == 'list':
            await list_teachers(session)
        elif args.action == 'update':
            await update_teacher(session, args.id, args.first_name, args.last_name)
        elif args.action == 'remove':
            await delete_teacher(session, args.id)
