import sqlite3

def execute_query():
    with open('query_0.sql', 'r') as f:
        sql = f.read()

    with sqlite3.connect('study.db') as con:
        cur = con.cursor()
        cur.execute(sql)
        return cur.fetchall()

print(execute_query())