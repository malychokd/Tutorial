import datetime

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Mapped

import psycopg2
DATABASE_URL = f"postgresql+psycopg2://postgres:secret@db:5432/postgres" 

engine = create_engine(DATABASE_URL, echo=False)
# engine = create_engine('sqlite:////study.db', echo=False)
DBSession = sessionmaker(bind=engine)
session = DBSession()

Base = declarative_base()

class Group(Base):
    __tablename__ = "group_students"
    id = Column(Integer, primary_key=True)
    group_name = Column(String(250), nullable=False)

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    student = Column(String(250), nullable=False)
    group_id = Column(Integer, ForeignKey('group_students.id'))
    group = relationship(Group, backref="students")

class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True)
    teacher = Column(String(250), nullable=False)
    
class Subject(Base):
    __tablename__ = "subjects"
    id = Column(Integer, primary_key=True)
    subject_name = Column(String(250), nullable=False)
    teacher_id = Column(Integer, ForeignKey('teachers.id'))
    teacher = relationship(Teacher, backref="subjects")

class Evaluations(Base):
    __tablename__ = "evaluations"
    id = Column(Integer, primary_key=True)
    data_eval = Column(DateTime, default=datetime.datetime.utcnow)
    evaluation = Column(Integer)
    student_id = Column(Integer, ForeignKey('students.id'))
    student = relationship(Student, backref="grades")

    subject_id = Column(Integer, ForeignKey('subjects.id'))
    subject = relationship(Subject, backref="grades")

# Base.metadata.create_all(engine)
Base.metadata.bind = engine