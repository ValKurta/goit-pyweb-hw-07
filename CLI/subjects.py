import asyncio
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, delete
from models import Subjects
from database import get_async_session


async def create_subject(session: AsyncSession, name: str, teacher_id: int):
    subject = Subjects(Subject_Name=name, Teacher_ID=teacher_id)
    session.add(subject)
    await session.commit()
    print(f"Subject {name} created.")


async def list_subjects(session: AsyncSession):
    result = await session.execute(select(Subjects))
    subjects = result.scalars().all()
    for subject in subjects:
        print(f"ID: {subject.Subject_ID}, Name: {subject.Subject_Name}, Teacher ID: {subject.Teacher_ID}")


async def update_subject(session: AsyncSession, subject_id: int, name: str, teacher_id: int):
    await session.execute(
        update(Subjects)
        .where(Subjects.Subject_ID == subject_id)
        .values(Subject_Name=name, Teacher_ID=teacher_id)
    )
    await session.commit()
    print(f"Subject with ID {subject_id} updated.")


async def delete_subject(session: AsyncSession, subject_id: int):
    await session.execute(delete(Subjects).where(Subjects.Subject_ID == subject_id))
    await session.commit()
    print(f"Subject with ID {subject_id} deleted.")


async def subject_operations(args):
    async with get_async_session() as session:
        if args.action == 'create':
            await create_subject(session, args.name, args.teacher_id)
        elif args.action == 'list':
            await list_subjects(session)
        elif args.action == 'update':
            await update_subject(session, args.id, args.name, args.teacher_id)
        elif args.action == 'remove':
            await delete_subject(session, args.id)
