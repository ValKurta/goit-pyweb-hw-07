import asyncio
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, delete
from models import Groups
from database import get_async_session


async def create_group(session: AsyncSession, name: str):
    group = Groups(Group_Name=name)
    session.add(group)
    await session.commit()
    print(f"Group {name} created.")


async def list_groups(session: AsyncSession):
    result = await session.execute(select(Groups))
    groups = result.scalars().all()
    for group in groups:
        print(f"ID: {group.Group_ID}, Name: {group.Group_Name}")


async def update_group(session: AsyncSession, group_id: int, name: str):
    await session.execute(
        update(Groups)
        .where(Groups.Group_ID == group_id)
        .values(Group_Name=name)
    )
    await session.commit()
    print(f"Group with ID {group_id} updated.")


async def delete_group(session: AsyncSession, group_id: int):
    await session.execute(delete(Groups).where(Groups.Group_ID == group_id))
    await session.commit()
    print(f"Group with ID {group_id} deleted.")


async def group_operations(args):
    async with get_async_session() as session:
        if args.action == 'create':
            await create_group(session, args.name)
        elif args.action == 'list':
            await list_groups(session)
        elif args.action == 'update':
            await update_group(session, args.id, args.name)
        elif args.action == 'remove':
            await delete_group(session, args.id)
