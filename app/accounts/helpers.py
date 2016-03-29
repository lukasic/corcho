# -*- coding: utf-8 -*-

def is_student(user):
    return user.groups.filter(name='student').exists()

def is_teacher(user):
    return user.groups.filter(name='teacher').exists()
