# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from app.accounts.models import Teacher, Student


class CourseCategory(models.Model):
    """
    Course Category - Subject, Seminar, Optional seminar...
    Used later when configuring couses choosing.
    """

    class Meta:
        verbose_name = _("Course category")
        verbose_name_plural = _("Course categories")

    acronym = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=False, blank=True, default="")

    def __str__(self):
        return self.name


class SubjectClass(models.Model):
    """
    Subject class - e.g Math, Biology, ...
    Every course must have unique Subject Class.
    """

    class Meta:
        verbose_name = _("Subject class")
        verbose_name_plural = _("Subject classes")

    acronym = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100, unique=True)
    teachers = models.ManyToManyField(to=Teacher, blank=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    """
    Course for specific grade/year. It's better to distinquish it.
    Course does not have grade as attribute, becouse some courses can be
    independed from year, e.g. optional couse: Cisco CCNA.

    Examples:
      - (03-MATH) Maths for 3th year
      - (03-SEM) Maths seminar for 3th year
      - (04-SEM) Maths seminar for 4th year
    """

    class Meta:
        ordering = ("-active", "acronym",)
        unique_together = ("name", "category")
        verbose_name = _("Course")
        verbose_name_plural = _("Courses")

    active = models.BooleanField(default=True)
    category = models.ForeignKey(to=CourseCategory)
    subject_class = models.ForeignKey(to=SubjectClass)
    acronym = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    teachers = models.ManyToManyField(to=Teacher, blank=True)
    info_goal = models.CharField(max_length=512, blank=True, default="")
    info_content = models.CharField(max_length=512, blank=True, default="")
    info_anotations = models.TextField(blank=True, default="")

    def __str__(self):
        return self.acronym + ": " + self.name

    def teachers_str(self):
        return ', '.join(teacher.user.get_full_name() for teacher in self.teachers.all()) or None

