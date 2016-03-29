# -*- coding: utf-8 -*-

from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test

from app.accounts.helpers import is_student
from app.courses.models import Course, CourseCategory
from app.choosing.models import Choosing, Choose, ChoosingPhase
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
