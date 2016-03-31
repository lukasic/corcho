# -*- coding: utf-8 -*-

from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test

from app.accounts.helpers import is_student
from app.courses.models import Course, CourseCategory
from app.choosing.models import Choosing, Choose, ChoosingPhase, TeacherRequest
from app.choosing.helpers import get_student_choosings


@login_required
@user_passes_test(is_student)
def phase2_choosing(request):
    confs = get_student_choosings(request.user.student)
    print(confs)

    groups = list()
    for choosing in confs:
        choosed_courses = dict()
        denied_courses = choosing.denied_courses.all()
        chooses_count = 0

        chooses = Choose.objects.filter(choosing=choosing, student__user=request.user).all()
        for c in chooses:
            #if c.phase != ChoosingPhase.CHOOSES_EVALUATING_2:
            choosed_courses[ c.course.id ] = c
            if c.phase != 2:
                chooses_count += 1

        rows = list()
        for course in choosing.course_category.course_set.all():
            choose = None
            if course.id in choosed_courses.keys():
                choose = choosed_courses[ course.id ]
            rows.append({ 'course': course, 'choose': choose })

        groups.append({
            'choosing': choosing,
            'rows': rows,
            'chooses': choosed_courses,
            'chooses_count': chooses_count,
            'denied_courses': denied_courses,
            'course_set': choosing.course_category.course_set
        })

    context = {
        'groups': groups
    }

    return render(request, "student/phase2_choosing.html", context)


@login_required
@user_passes_test(is_student)
def my_courses(request):
    confs = get_student_choosings(request.user.student)
    groups = []

    for choosing in confs:
        chooses = Choose.objects.filter(choosing=choosing, student__user=request.user)
        groups.append({'choosing': choosing, 'chooses':chooses})

    context = {
        'groups': groups
    }

    return render(request, 'student/my_courses.html', context)


@login_required
@user_passes_test(is_student)
def teachers_requests(request):
    confs = get_student_choosings(request.user.student)
    groups = []

    for choosing in confs:
        if not choosing.allow_teacher_requests:
            continue
        chooses = Choose.objects.filter(choosing=choosing, student__user=request.user)
        reqs = TeacherRequest.objects.filter(choose__in=chooses).all()
        groups.append({'choosing':choosing, 'chooses':chooses, 'requests':reqs, 'denied_courses': choosing.denied_courses.all()})

    context = {
        'groups': groups,
    }

    return render(request, "student/teachers_requests.html", context)

