from models import Student, Group, Subject, Teacher, Evaluations, session
from faker import Faker 
import random

NUMBER_GROUP_STUDENTS = 3 #group_students
NUMBER_STUDENTS = 50 #students
NUMBER_SUBJECTS = 8 #subjects
NUMBER_TEACHERS = 5 #teachers
NUMBER_EVALUATIONS = 2000 #evaluations 8000

groups_list = list()
for _ in range(NUMBER_GROUP_STUDENTS):
    group = Group(group_name=Faker().bothify(letters='ABCDE'))
    groups_list.append(group)
    session.add(group)
session.commit()
print('Додано групи')

students_list = list()
for _ in range(NUMBER_STUDENTS):
    student = Student(student=Faker().name(), group=random.choice(groups_list))
    students_list.append(student)
    session.add(student)
session.commit()
print('Додано студентів')

teachers_list = list()
for _ in range(NUMBER_TEACHERS):
    teacher = Teacher(teacher=Faker().name())
    teachers_list.append(teacher)
    session.add(teacher)
session.commit()
print('Додано викладачів')

subjects_list = list()
for _ in range(NUMBER_SUBJECTS):
    subject = Subject(subject_name=Faker().catch_phrase(), teacher=random.choice(teachers_list))
    subjects_list.append(subject)
    session.add(subject)
session.commit()
print('Додано предмети')

print('Додаю оцінки...')
eval_list = list()
for i in range(5):
    eval_list.append(i+1)

evaluations_list = list()
for _ in range(NUMBER_EVALUATIONS):
    evaluation = Evaluations(data_eval=Faker().date_between(start_date='-1y', end_date='today'), evaluation=random.choice(eval_list), student=random.choice(students_list), subject=random.choice(subjects_list))
    session.add(evaluation)
session.commit()
print('Оцінки додано. Наповнення бази завершено!')    
