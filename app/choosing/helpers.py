# -*- coding: utf-8 -*-

from app.choosing.models import Choosing
from app.accounts.helpers import is_student

def get_student_choosings(student):
    grade = student.classroom.grade
    confs = Choosing.get_active_for_grade(grade)
    confs += Choosing.get_active_for_grade(None)
    return confs


def get_user_choosings(user):
	if not is_student(user):
		raise RuntimeError()
	return get_student_choosings(user.student)

