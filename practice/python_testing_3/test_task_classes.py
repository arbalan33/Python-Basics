"""
Write tests for classes in 2_python_part_2/task_classes.py (Homework, Teacher, Student).
Check if all methods working correctly.
Also check corner-cases, for example if homework number of days is negative.
"""

import pytest
import time
import datetime
from ..python_part_2.task_classes import *


def test_homework_expiration():
    homework = Homework('Learn functions', datetime.timedelta(days=1))
    assert homework.is_active()

    expired_homework = Homework('Learn functions', datetime.timedelta(milliseconds=1))
    time.sleep(0.1)
    assert not expired_homework.is_active()


def test_homework_negative_date():
    homework = Homework('Learn functions', datetime.timedelta(days=-1))
    assert not homework.is_active()


def test_student_homework():
    student = Student("lastname", "firstname")
    homework = Homework('Learn functions', datetime.timedelta(days=1))
    assert student.do_homework(homework) == homework


def test_student_expired_homework(capsys):
    student = Student("lastname", "firstname")
    expired_homework = Homework('Learn functions', datetime.timedelta(milliseconds=1))
    time.sleep(0.1)

    assert student.do_homework(expired_homework) is None
    captured = capsys.readouterr()
    assert captured.out == 'You are late\n'


def test_teacher():
    teacher = Teacher('Dmitry', 'Orlyakov')
    expired_homework = Teacher.create_homework('Learn functions', 0)
    time.sleep(0.1)
    assert not expired_homework.is_active()


def test_scenario():
    teacher = Teacher('Dmitry', 'Orlyakov')
    student = Student('Vladislav', 'Popov')
    assert teacher.last_name == 'Dmitry'
    assert student.first_name == 'Popov'

    expired_homework = Teacher.create_homework('Learn functions', 0)
    assert isinstance(expired_homework.created, datetime.datetime)
    assert expired_homework.deadline  == datetime.timedelta()
    assert expired_homework.text == 'Learn functions'

    # create function from method and use it
    create_homework_too = Teacher.create_homework
    oop_homework = create_homework_too('create 2 simple classes', 5)
    oop_homework.deadline  # 5 days, 0:00:00

    assert student.do_homework(oop_homework) == oop_homework
    assert student.do_homework(expired_homework) is None  # You are late
