from sqlalchemy import *

from models import Student, Group, Subject, Teacher, Evaluations, session

def select_1():
    stmt = (select(Student.student, func.round(func.avg(Evaluations.evaluation), 2).label('evaluation'))
            .join(Student)
            .group_by(Student.student).order_by(desc('evaluation')).limit(5))
    result = session.execute(stmt).all()
    for eval in result:
        print(eval.student, eval.evaluation)
    
def select_2():
    stmt = (select(Student.student, func.round(func.avg(Evaluations.evaluation), 2).label('evaluation'))
            .join(Student)
            .where(Evaluations.subject_id == 8)
            .group_by(Student.student).order_by(desc('evaluation')).limit(1))
    result = session.execute(stmt).all()
    for eval in result:
        print(eval.student, eval.evaluation)

def select_3():
    stmt = (select(Group.group_name, func.round(func.avg(Evaluations.evaluation), 2).label('evaluation'))
            .join(Student, Evaluations.student_id == Student.id).join(Group, Student.group_id == Group.id)
            .where(Evaluations.subject_id == 8)
            .group_by(Group.group_name))
    result = session.execute(stmt).all()
    for eval in result:
        print(eval.group_name, eval.evaluation)

def select_4():
    stmt = (select(func.round(func.avg(Evaluations.evaluation), 2).label('evaluation')))
    result = session.execute(stmt).all()
    for eval in result:
        print(eval.evaluation)

def select_5():
    stmt = (select(Subject.subject_name)
        .where(Subject.teacher_id == 5))
    result = session.execute(stmt).all()
    for eval in result:
        print(eval.subject_name)

def select_6():
    stmt = (select(Student.student)
        .where(Student.group_id == 3))
    result = session.execute(stmt).all()
    for eval in result:
        print(eval.student)

def select_7():
    stmt = (select(Student.student, Evaluations.evaluation)
        .join(Student, Evaluations.student_id == Student.id)
        .where(and_(Student.group_id == 3, Evaluations.subject_id == 8)))
    result = session.execute(stmt).all()
    for eval in result:
        print(eval.student, eval.evaluation)

def select_8():
    stmt = (select(Teacher.teacher, func.round(func.avg(Evaluations.evaluation), 2).label('evaluation'))
        .join(Subject, Evaluations.subject_id == Subject.id)
        .join(Teacher, Subject.teacher_id == Teacher.id)
        .where(Subject.teacher_id == 5)
        .group_by(Teacher.teacher))
    result = session.execute(stmt).all()
    for eval in result:
        print(eval.teacher, eval.evaluation)

def select_9():
    stmt = (select(Subject.subject_name)
        .select_from(Evaluations)
        .join(Subject, Evaluations.subject_id == Subject.id)
        .where(Evaluations.student_id == 1)
        .group_by(Subject.subject_name))
    result = session.execute(stmt).all()
    for eval in result:
        print(eval.subject_name)

def select_10():
    stmt = (select(Subject.subject_name)
        .select_from(Evaluations)
        .join(Subject, Evaluations.subject_id == Subject.id)
        .where(and_(Evaluations.student_id == 50, Subject.teacher_id == 5))
        .group_by(Subject.subject_name))
    result = session.execute(stmt).all()
    for eval in result:
        print(eval.subject_name)

def select_11():
    stmt = (select(func.round(func.avg(Evaluations.evaluation), 2).label('evaluation'))
        .select_from(Evaluations)
        .join(Subject, Evaluations.subject_id == Subject.id)
        .where(and_(Evaluations.student_id == 35, Subject.teacher_id == 4)))
    result = session.execute(stmt).all()
    for eval in result:
        print(eval.evaluation)

def select_12():

    max_date_eval = (select(func.max(Evaluations.data_eval))
    .where(and_(Evaluations.student_id == Student.id, Evaluations.subject_id == Subject.id))
    .correlate(Student)
    .correlate(Subject)
    .scalar_subquery())

    stmt = (select(Student.id, Student.student.label('student_name'), Subject.subject_name.label('subject_name'), Evaluations.evaluation.label('student_eval'), Evaluations.data_eval)
        .select_from(Student)
        .join(Group, Student.group_id == Group.id)
        .join(Evaluations, Student.id == Evaluations.student_id)
        .join(Subject, Evaluations.subject_id == Subject.id)
        .where(and_(Group.id == 1, Subject.id == 1, Evaluations.data_eval == max_date_eval))
        .order_by('student_name'))

    result = session.execute(stmt).all()
    for eval in result:
        print(eval.id, eval.student_name, eval.subject_name, eval.student_eval, eval.data_eval)

select_12()