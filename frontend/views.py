# -*- coding: utf-8 -*-

from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required, user_passes_test

from app.accounts.models import Student, Teacher
from app.accounts.helpers import is_student, is_teacher
from app.courses.models import Course, CourseCategory
from app.choosing.models import Choosing, Choose, ResolvedCourse, TeacherRequest, ResolvedCombination

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


class CourseTeacherOverview:
    teacher = None
    requests = None
    accepted = None
    resolution = None

    def size():
        doc = "The size property."
        def fget(self):
            return len(self.requests)
        return locals()
    size = property(**size())


class CourseOverview:
    course = None
    accepted = None
    resolution = None
    size = None
    teachers = None
    noteachers = None

    def __init__(self):
        self.size = 0
        self.teachers = dict()
        self.noteachers = list()

    def _add_request(self, request):
        key = request.teacher
        if key not in self.teachers.keys():
            cttr = CourseTeacherOverview()
            cttr.teacher = request.teacher
            cttr.requests = list()
            self.teachers[key] = cttr
        self.teachers[key].requests.append(request)

    def add_choose(self, choose):
        course = choose.course
        requests = choose.teacherrequest_set
        self.size += 1
        if requests.count() == 1:
            self._add_request(requests.get())
        elif requests.count() == 0:
            self.noteachers.append(choose)
        else:
            raise RuntimeError("Assert - choose has more than one teacher requests!")

    def update_resolution(self, resolution):
        self.accepted = resolution.accepted
        self.resolution = resolution

    def update_teacher_resolution(self, combination):
        teacher = combination.teacher
        if teacher not in self.teachers.keys():
            return
        self.teachers[teacher].accepted = combination.accepted
        self.teachers[teacher].resolution = combination

    def clear_resolutions(self):
        self.accepted = None
        self.resolution = None
        for teacher, teacher_ow in self.teachers.items():
            teacher_ow.accepted = None
            teacher_ow.resolution = None


class ChoosingOverview:

    def __init__(self, choosing):
        self.choosing = choosing
        self.incomplete = list()
        self.courses = dict()

    def _set_course_resolution(self, resolution):
        course = resolution.course
        self.courses[course].update_resolution(resolution)

    def _set_courseteacher_resolution(self, combination):
        course = combination.course
        if course not in self.courses.keys():
            return
        self.courses[course].update_teacher_resolution(combination)

    def generate(self):
        # process students, chooses, requests
        for student in Student.objects.filter(classroom__grade=self.choosing.for_grade):
            chooses = student.choose_set.filter(choosing=self.choosing)
            valid_cnt = chooses.exclude(phase=2).count()
            if valid_cnt < self.choosing.courses_min or valid_cnt > self.choosing.courses_max:
                self.incomplete.append((student, valid_cnt))

            for choose in chooses:
                course = choose.course
                if course not in self.courses:
                    self.courses[course] = CourseOverview()
                    self.courses[course].course = course

                self.courses[course].add_choose(choose)


    def reload_resolutions(self):
        # append resolutions
        for course, course_ow in self.courses.items():
            course_ow.clear_resolutions()

        for c in ResolvedCourse.objects.filter(choosing=self.choosing):
            self._set_course_resolution(c)

        for c in ResolvedCombination.objects.filter(choosing=self.choosing):
            self._set_courseteacher_resolution(c)


class ChoosingOverviewFactory:

    cache = dict()

    @staticmethod
    def purge():
        ChoosingOverviewFactory.cache = dict()

    @staticmethod
    def get(choosing):
        if choosing.id not in ChoosingOverviewFactory.cache.keys():
            overview = ChoosingOverview(choosing)
            overview.generate()
            overview.reload_resolutions()
            ChoosingOverviewFactory.cache[choosing.id] = overview

        overview = ChoosingOverviewFactory.cache[choosing.id]
        overview.reload_resolutions()
        return overview


@login_required
def overview(request, choosing_id = None):

    if request.user.is_superuser == False:
        raise "Access denied."

    if 'purge' in request.GET.keys():
        ChoosingOverviewFactory.purge()
        return redirect(overview, choosing_id)

    context = {}

    choosing = None
    if choosing_id:
        choosing = Choosing.objects.get(id=int(choosing_id))
        context['cur_choosing'] = choosing

    context['choosing_list'] = Choosing.objects.all()

    if choosing and choosing.phase in (1,2,3):
        context['overview'] = ChoosingOverviewFactory.get(choosing)

    return render_to_response("root/overview.html", context, RequestContext(request))

