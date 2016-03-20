# -*- coding: utf-8 -*-

"""
Extension of django.contrib.auth.models.User model.
Specialization of users for studnents and teachers.
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _


class Classroom(models.Model):

    class Meta:
        unique_together = ('grade', 'name')
        ordering = ('grade', 'name')

    grade = models.IntegerField()
    name = models.CharField(max_length=10)

    def __str__(self):
        return "{0}.{1}".format(self.grade, self.name)


class Student(models.Model):
    """
    User specialization - Student Profile.
    """

    class Meta:
        verbose_name = _("Student")
        verbose_name_plural = _("Students")
        ordering = ('classroom', 'user')

    user = models.OneToOneField(to=User)
    classroom = models.ForeignKey(to=Classroom)

    def __repr__(self):
        return "<Student: {0} ({1})>".format(self.user.username, str(self.classroom))

    def __str__(self):
        return self.user.get_full_name()


class Teacher(models.Model):
    """
    User specialization - Teacher Profile
    """

    class Meta:
        verbose_name = _("Teacher")
        verbose_name_plural = _("Teachers")

    user = models.OneToOneField(to=User)
    titles_before = models.CharField(max_length=50, blank=True, null=False, default="")
    titles_after = models.CharField(max_length=50, blank=True, null=False, default="")
    #classroom = models.ForeignKey(to=Classroom, blank=True, null=True, related_name="classmaster")

    def subjects_list(self):
        return ', '.join(s.acronym for s in self.subjectclass_set.all())
    subjects_list.short_description = _("subjects")

    def courses_list(self):
        return ', '.join(s.acronym for s in self.course_set.all())
    courses_list.short_description = _("courses")

    def get_titled_name(self):
        out = ""
        if self.titles_before:
            out = self.titles_before + " "
        out += self.user.get_full_name()
        if self.titles_after:
            out += ", " + self.titles_after
        return out
    get_titled_name.short_description = _("name")

    def __repr__(self):
        return "<Teacher: {0}>".format(self.user.username)

    def __str__(self):
        return self.get_titled_name()

