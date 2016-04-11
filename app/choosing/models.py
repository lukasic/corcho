# -*- coding: utf-8 -*-

"""
Practical core of application - configuration and student's choices.
"""

from datetime import datetime

from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from app.accounts.models import Student, Teacher
from app.courses.models import Course, CourseCategory

# also import in Choose.clean function:
#   from app.choosing.helpers import get_student_choosings


class ChoosingPhase:
    PREPARING_0 = 0
    COURSES_CHOOSING_1 = 1
    CHOOSES_EVALUATING_2 = 2
    CHOOSES_CHANING_3 = 3
    GROUPS_CREATING_4 = 4
    GROUPS_CHANGES_5 = 5
    FINISHED_6 = 6

CHOOSING_PHASE = (
    (ChoosingPhase.PREPARING_0,           _("Preparation")),
    (ChoosingPhase.COURSES_CHOOSING_1,    _("Choosing of courses")),
    (ChoosingPhase.CHOOSES_EVALUATING_2,  _("Evaluating of options")),
    (ChoosingPhase.CHOOSES_CHANING_3,     _("Changes in choosings")),
    (ChoosingPhase.GROUPS_CREATING_4,     _("Creating groups")),
    (ChoosingPhase.GROUPS_CHANGES_5,      _("Group changes")),
    (ChoosingPhase.FINISHED_6,            _("Finished"))
)


class Choosing(models.Model):
    """
    Configuration of choosing - we distinquish between choosing subjects and seminars,
    also between years / grades.
    """

    class Meta:
        ordering = ("priority",)
        verbose_name = _("Choosing configuration")
        verbose_name_plural = _("Choosing configurations")


    acronym = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, default="")
    #schoolyear = models.CharField(max_length=9, null=False, blank=False)

    #
    # Management
    #
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()
    phase = models.IntegerField(choices=CHOOSING_PHASE)
    active = models.BooleanField(default=True)

    # Allow requesting for teacher?
    allow_teacher_requests = models.BooleanField(default=False)

    # Which courses can be choosed - and how many.
    course_category = models.ForeignKey(to=CourseCategory)
    courses_min = models.IntegerField()
    courses_max = models.IntegerField()

    # Helper fields
    priority = models.IntegerField()
    for_grade = models.IntegerField(null=True, blank=True, default=None)

    # Courses not opened because of low interest - for phase 3.
    denied_courses = models.ManyToManyField(Course, blank=True)

    def __str__(self):
        return self.name

    def get_chooses_for(self, student_id):
        return self.choose_set.filter(student__id=student_id).all()

    def resolve_courses(self):
        courses = []
        for course in self.course_category.course_set.all():
            if course not in self.denied_courses.all():
                courses.append(course)

        return courses

    @staticmethod
    def get_active_for_grade(grade):
        l = list()

        all_active = Choosing.objects.filter(active=True, for_grade=grade,
            time_start__lte=datetime.now(), time_end__gte=datetime.now()
        ).all()

        for c in all_active:
            l.append(c)

        return l


CHOOSE_PHASE = (
    (0, _("Waiting")),
    (1, _("Approved")),
    (2, _("Denied")),
    (3, _("Deleted"))
)


class Choose(models.Model):
    """
    Student's couse choose.
    """

    class Meta:
        verbose_name = _("Student's choose")
        verbose_name_plural = _("Students' chooses")
        unique_together = ('student', 'choosing', 'course')

    student = models.ForeignKey(to=Student)
    choosing = models.ForeignKey(to=Choosing)
    course = models.ForeignKey(to=Course)
    created_at = models.DateTimeField(auto_now_add=True)
    phase = models.IntegerField(choices=CHOOSE_PHASE, default=0)

    def clean(self):
        from app.choosing.helpers import get_student_choosings

        student_choosing_set = get_student_choosings(self.student)
        if self.choosing not in student_choosing_set:
            raise ValidationError(_('Student cannot choose in this choosing.'))

        if self.course not in self.choosing.course_category.course_set.all():
            raise ValidationError(_('Course does not belong to the choosing course category.'))

        others_count = Choose.objects.filter(student=self.student, choosing=self.choosing, phase__lt=2).count()
        if self.id:
            others_count -= 1

        if others_count >= self.choosing.courses_max:
            raise ValidationError(_('Student reached maximum limit of choosed courses.'))

        if self.phase == 3:
            return
        if self.choosing.phase in (0, 1):
            return
        if self.course in self.choosing.denied_courses.all():
            if self.phase == 2:
                return
            raise ValidationError(_('Could not choose denied course.'))

    def __repr__(self):
        return "<Choose: %d>" % self.id

    def __str__(self):
        return "%s / %s" % (self.student, self.course.name)

    @property
    def phase_str(self):
        for phase in CHOOSE_PHASE:
            if phase[0] == self.phase:
                return phase[1]
        return "N/A"

    @property
    def cancelable(self):
        if self.choosing.phase in (0,2,4,6):
            return False
        return True if self.phase == 0 else False

    def is_owner(self, user):
        return user.student and self.student == user.student

    def accept(self):
        self.phase = 1
        self.save()

    def reject(self):
        self.phase = 2
        if self.teacherrequest_set.all() > 0:
            for req in self.teacherrequest_set.all():
                req.phase = 2
                req.save()
        self.save()


TEACHER_REQUEST_PHASE = (
    (0, _("Waiting")),
    (1, _("Approved")),
    (2, _("Denied"))
)


class TeacherRequest(models.Model):
    """
    Student wants specific teacher, but there are no guarantees because
    of time-table integration restrictions.
    """

    class Meta:
        verbose_name = _("Request for teacher")
        verbose_name_plural = _("Requests for teachers")

    choose = models.ForeignKey(to=Choose)
    teacher = models.ForeignKey(to=Teacher)
    phase = models.IntegerField(choices=TEACHER_REQUEST_PHASE, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.choose)

    @property
    def phase_str(self):
        for phase in CHOOSE_PHASE:
            if phase[0] == self.phase:
                return phase[1]
        return "N/A"

    @property
    def cancelable(self):
        if self.choose.choosing.phase in (0,2,4,6):
            return False
        return True if self.phase == 0 else False


class DeniedCombination(models.Model):
    """
    Combinations of course-teacher, which does not have sufficient interest
    and therefore this (teacher) requests will be denied.
    """

    choosing = models.ForeignKey(Choosing)
    course = models.ForeignKey(Course)
    teacher = models.ForeignKey(Teacher)

    class Meta:
        unique_together = ('choosing', 'course', 'teacher')

    def clean(self):
        if self.course not in self.choosing.course_category.course_set.all():
            raise ValidationError("Course is not associated with choosing.")

        if self.teacher not in self.course.teachers.all():
            raise ValidationError("Selected teacher does not teach this course.")

    def __str_(self):
        return "{} / {}".format(self.course, self.teacher)

