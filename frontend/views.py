# -*- coding: utf-8 -*-

from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required, user_passes_test

from app.accounts.helpers import is_student, is_teacher
from app.courses.models import Course, CourseCategory

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

