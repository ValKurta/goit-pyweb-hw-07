import argparse
import asyncio
from CLI.teachers import teacher_operations
from CLI.groups import group_operations
from CLI.subjects import subject_operations
from CLI.students import student_operations
from CLI.grades import grade_operations


async def main(args):
    if args.model == 'Teacher':
        await teacher_operations(args)
    elif args.model == 'Group':
        await group_operations(args)
    elif args.model == 'Subject':
        await subject_operations(args)
    elif args.model == 'Student':
        await student_operations(args)
    elif args.model == 'Grade':
        await grade_operations(args)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CRUD operations with database.")
    parser.add_argument('-a', '--action', choices=['create', 'list', 'update', 'remove'], required=True, help="CRUD")
    parser.add_argument('-m', '--model', choices=['Teacher', 'Group', 'Subject', 'Student', 'Grade'], required=True, help="Model to run")

    parser.add_argument('--first_name', type=str, help="First name of the teacher or student")
    parser.add_argument('--last_name', type=str, help="Last name of the teacher or student")
    parser.add_argument('--name', type=str, help="Name of the group or subject")
    parser.add_argument('--id', type=int, help="ID of the record to update or delete")
    parser.add_argument('--teacher_id', type=int, help="Teacher ID for subject")
    parser.add_argument('--group_id', type=int, help="Group ID for student")
    parser.add_argument('--date_of_birth', type=str, help="Date of birth for student")
    parser.add_argument('--student_id', type=int, help="Student ID for grade")
    parser.add_argument('--subject_id', type=int, help="Subject ID for grade")
    parser.add_argument('--grade', type=int, help="Grade value")
    parser.add_argument('--date_received', type=str, help="Date received for grade")

    args = parser.parse_args()

    asyncio.run(main(args))
