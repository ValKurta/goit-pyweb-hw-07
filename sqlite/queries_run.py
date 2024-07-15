import sqlite3
import os

con = sqlite3.connect('school.db')
cur = con.cursor()

queries_dir = './sql'

def execute_sql_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        sql = file.read()
        cur.execute(sql)
        rows = cur.fetchall()

        print(f"SQL script from {filename}:\n{sql}\nResults from {filename}:")
        for row in rows:
            print(row)


for i in range(1, 13):
    filename = os.path.join(queries_dir, f'query_{i}.sql')
    if os.path.isfile(filename):
        execute_sql_file(filename)
        print("---")
    else:
        print(f"File {filename} does not exist.")

con.close()
