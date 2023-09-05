from models import Student, Group, Subject, Teacher, Evaluations, session

import argparse
import datetime

parser = argparse.ArgumentParser(description="CRUD operations for database models")

parser.add_argument("--action", "-a", choices=["create", "list", "update", "remove"], required=True, help="Action to perform")
parser.add_argument("--model", "-m", choices=["Teacher", "Student", "Group", "Subject", "Evaluations"], required=True, help="Model to operate on")

parser.add_argument("--name", "-n", help="Name for the record")
parser.add_argument("--eval", type=int, help="Eval of the record")
parser.add_argument("--group_id", type=int, help="group_id of the record")
parser.add_argument("--data_eval", type=datetime.date, help="data_eval of the record")
parser.add_argument("--teacher_id", type=int, help="teacher_id of the record")
parser.add_argument("--student_id", type=int, help="student_id of the record")
parser.add_argument("--subject_id", type=int, help="subject_id of the record")
parser.add_argument("--eval_id", type=int, help="eval_id of the record")

args = parser.parse_args()

if args.action == "create":
    if args.model == "Teacher":
        # Операція створення вчителя
        teacher = Teacher(teacher=args.name)
        session.add(teacher)
        session.commit()
        print("Teacher created successfully.")
    elif args.model == "Student":
        # Операція створення студента
        student = Student(student=args.name, group_id=args.group_id)
        session.add(student)
        session.commit()
        print("Student created successfully.")
    elif args.model == "Group":
        # Операція створення групи
        group = Group(group_name=args.name)
        session.add(group)
        session.commit()
        print("Group created successfully.")
    elif args.model == "Subject":
        # Операція створення предмету
        subject = Subject(subject_name=args.name, teacher_id=args.teacher_id)
        session.add(subject)
        session.commit()
        print("Subject created successfully.")
    elif args.model == "Evaluations":
        # Операція створення оцінок
        evaluation = Evaluations(data_eval=args.data_eval, evaluation=args.eval, student_id=args.student_id, subject_id=args.subject_id)
        session.add(evaluation)
        session.commit()
        print("Evaluation created successfully.")        

elif args.action == "list":
    if args.model == "Teacher":
        # Операція отримання списку вчителів
        teachers = session.query(Teacher).all()
        for teacher in teachers:
            print(f"ID: {teacher.id}, Name: {teacher.teacher}")
    elif args.model == "Student":
        # Операція отримання списку студентів
        students = session.query(Student).all()
        for student in students:
            print(f"ID: {student.id}, Name: {student.student}, Group id: {student.group_id}")
    elif args.model == "Group":
        # Операція отримання списку груп
        groups = session.query(Group).all()
        for group in groups:
            print(f"ID: {group.id}, Name: {group.group_name}")
    elif args.model == "Subject":
        # Операція отримання списку предметів
        subjects = session.query(Subject).all()
        for subject in subjects:
            print(f"ID: {subject.id}, Name: {subject.subject_name}, Teacher id: {subject.teacher_id}") 
    elif args.model == "Evaluations":
        # Операція отримання списку оцінок
        evaluations = session.query(Evaluations).all()
        for evaluation in evaluations:
            print(f"ID: {evaluation.id}, Evaluation: {evaluation.evaluation}, Data: {evaluation.data_eval}, Student id: {evaluation.student_id}, Subject id: {evaluation.subject_id}")                     

elif args.action == "update":
    if args.model == "Teacher":
        # Операція оновлення даних вчителя за id
        teacher = session.query(Teacher).filter_by(id=args.teacher_id).first()
        if teacher:
            teacher.teacher = args.name
            session.commit()
            print("Teacher updated successfully.")
        else:
            print("Teacher not found.")
    elif args.model == "Student":
        # Операція оновлення даних студента за id
        student = session.query(Student).filter_by(id=args.student_id).first()
        if student:
            student.student = args.name
            student.group_id = args.group_id
            session.commit()
            print("Student updated successfully.")
        else:
            print("Student not found.")
    elif args.model == "Group":
        # Операція оновлення даних групи за id
        group = session.query(Group).filter_by(id=args.group_id).first()
        if group:
            group.group_name = args.name
            session.commit()
            print("Group updated successfully.")
        else:
            print("Group not found.")
    elif args.model == "Subject":
        # Операція оновлення даних предмета за id
        subject = session.query(Subject).filter_by(id=args.subject_id).first()
        if subject:
            subject.subject_name = args.name
            subject.teacher_id = args.teacher_id
            session.commit()
            print("Subject updated successfully.")
        else:
            print("Subject not found.")
    elif args.model == "Evaluations":
        # Операція оновлення даних оцінки за id
        evaluation = session.query(Evaluations).filter_by(id=args.eval_id).first()
        if evaluation:
            evaluation.evaluation = args.eval
            evaluation.data_eval = args.data_eval
            evaluation.student_id = args.student_id
            evaluation.subject_id = args.subject_id
            session.commit()
            print("Evaluation updated successfully.")
        else:
            print("Evaluation not found.")                     

elif args.action == "remove":
    if args.model == "Teacher":
        # Операція видалення вчителя за id
        teacher = session.query(Teacher).filter_by(id=args.teacher_id).first()
        if teacher:
            session.delete(teacher)
            session.commit()
            print("Teacher removed successfully.")
        else:
            print("Teacher not found.")
    elif args.model == "Student":
        # Операція видалення студента за id
        student = session.query(Student).filter_by(id=args.student_id).first()
        if student:
            session.delete(student)
            session.commit()
            print("Student removed successfully.")
        else:
            print("Student not found.")
    elif args.model == "Group":
        # Операція видалення групи за id
        group = session.query(Group).filter_by(id=args.group_id).first()
        if group:
            session.delete(group)
            session.commit()
            print("Group removed successfully.")
        else:
            print("Group not found.")
    elif args.model == "Subject":
        # Операція видалення предмета за id
        subject = session.query(Subject).filter_by(id=args.subject_id).first()
        if subject:
            session.delete(subject)
            session.commit()
            print("Subject removed successfully.")
        else:
            print("Subject not found.")
    elif args.model == "Evaluations":
        # Операція видалення оцінки за id
        evaluation = session.query(Evaluations).filter_by(id=args.eval_id).first()
        if evaluation:
            session.delete(evaluation)
            session.commit()
            print("Evaluation removed successfully.")
        else:
            print("Evaluation not found.")                
    

