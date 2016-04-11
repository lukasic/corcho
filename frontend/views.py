# -*- coding: utf-8 -*-

from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required, user_passes_test

from app.accounts.models import Student, Teacher
from app.accounts.helpers import is_student, is_teacher
from app.courses.models import Course, CourseCategory
from app.choosing.models import Choosing, Choose

from frontend import views_student
from frontend import views_teacher

@login_required
def dashboard(request):
    if is_student(request.user): return render(request, 'student/dashboard.html', {})
    if is_teacher(request.user): return render(request, 'teacher/dashboard.html', {})


def courses(request):
    context = {
        'categories': CourseCategory.objects.all(),
        'courses': Course.objects.filter(active=True),
    }
    return render(request, "pages/courses.html", context)


class A:
    pass

@login_required
def overview(request, choosing_id = None):

    if request.user.is_superuser == False:
        raise "Access denied."

    context = {}

    choosing = None
    if choosing_id:
        choosing = Choosing.objects.get(id=int(choosing_id))
        context['cur_choosing'] = choosing

    context['choosing_list'] = Choosing.objects.all()

    if choosing and choosing.phase in (1,2,3):
        students_map = {}
        invalid_students = []
        data = {}
        for student in Student.objects.filter(classroom__grade=choosing.for_grade):
            chooses = student.choose_set.filter(choosing=choosing).exclude(phase=2)
            if chooses.count() < choosing.courses_min or chooses.count() > choosing.courses_max:
                invalid_students.append( (student, chooses.count()) )
            for choose in chooses:
                course = choose.course
                req = choose.teacherrequest_set.all()
                if len(req) == 1:
                    req = req[0]
                    teacher = req.teacher
                    if course.id not in data.keys(): data[course.id] = {}
                    if teacher.id not in data[course.id].keys(): data[course.id][teacher.id] = []
                    data[course.id][teacher.id].append(req)

                elif len(req) == 0:
                    if course.id not in data.keys(): data[course.id] = {}
                    if -1 not in data[course.id].keys(): data[course.id][-1] = []
                    a = A()
                    a.choose = choose
                    a.teacher = None
                    data[course.id][-1].append(a)

                else:
                    raise RuntimeError("Assert - choose has more than one teacher requests!")

        context['invalid_students'] = invalid_students
        context['data'] = data


    return render_to_response("root/overview.html", context, RequestContext(request))
