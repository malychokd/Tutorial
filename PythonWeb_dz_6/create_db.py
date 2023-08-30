import sqlite3

from faker import Faker 
import random

NUMBER_GROUP_STUDENTS = 3 #group_students
NUMBER_STUDENTS = 50 #students
NUMBER_SUBJECTS = 8 #subjects
NUMBER_TEACHERS = 5 #teachers
NUMBER_EVALUATIONS = 2000 #evaluations 8000

def create_db():
    with open('init_db_study.sql', 'r') as f:
        sql = f.read()

    with sqlite3.connect('study.db') as con:
        cur = con.cursor()
        cur.executescript(sql)

# '''
# Заповніть отриману базу даних випадковими даними (~30-50 студентів, 3 групи, 5-8 предметів, 3-5 викладачів, до 20 оцінок у кожного студента з усіх предметів)
# '''
def populate_db():
    group_sql_command = "\n".join(f"INSERT INTO group_students (group_name) VALUES ('{Faker().bothify(letters='ABCDE')}');" for _ in range(NUMBER_GROUP_STUDENTS))
    #print(group_sql_command)
    with sqlite3.connect('study.db') as con:
        cur = con.cursor()
        cur.executescript(group_sql_command)
        cur.execute("SELECT id from group_students;")
        group_students_ids = [obj[0] for obj in cur.fetchall()]        
        #print(group_students_ids)
    print('Додано групи')

    students_sql_command = "\n".join(f"INSERT INTO students (student, group_id) VALUES ('{Faker().name()}', {random.choice(group_students_ids)});" for _ in range(NUMBER_STUDENTS))
    #print(students_sql_command)
    with sqlite3.connect('study.db') as con:
        cur = con.cursor()
        cur.executescript(students_sql_command)
        cur.execute("SELECT id from students;")
        students_ids = [obj[0] for obj in cur.fetchall()]        
        #print(students_ids)
    print('Додано студентів')

    teachers_sql_command = "\n".join(f"INSERT INTO teachers (teacher) VALUES ('{Faker().name()}');" for _ in range(NUMBER_TEACHERS))
    #print(teachers_sql_command)
    with sqlite3.connect('study.db') as con:
        cur = con.cursor()
        cur.executescript(teachers_sql_command)
        cur.execute("SELECT id from teachers;")
        teachers_ids = [obj[0] for obj in cur.fetchall()]        
        #print(teachers_ids)
    print('Додано викладачів')

    subjects_sql_command = "\n".join(f"INSERT INTO subjects (subject_name, teacher_id) VALUES ('{Faker().catch_phrase()}', {random.choice(teachers_ids)});" for _ in range(NUMBER_SUBJECTS))
    #print(subjects_sql_command)
    with sqlite3.connect('study.db') as con:
        cur = con.cursor()
        cur.executescript(subjects_sql_command)
        cur.execute("SELECT id from subjects;")
        subjects_ids = [obj[0] for obj in cur.fetchall()]        
        #print(subjects_ids)
    print('Додано предмети')    

    print('Додаю оцінки...')
    evaluations_sql_command = "\n".join(f"INSERT INTO evaluations (data_eval, evaluation, student_id, subject_id) VALUES ('{Faker().date_between(start_date='-1y', end_date='today')}', {random.choice(teachers_ids)}, {random.choice(students_ids)}, {random.choice(subjects_ids)});" for _ in range(NUMBER_EVALUATIONS))
    #print(evaluations_sql_command)
    with sqlite3.connect('study.db') as con:
        cur = con.cursor()
        cur.executescript(evaluations_sql_command)
        # cur.execute("SELECT id from evaluations;")
        # evaluations_ids = [obj[0] for obj in cur.fetchall()]        
        # print(evaluations_ids)
    print('Оцінки додано. Наповнення бази завершено!')

def init_db():
    create_db()
    populate_db()