# -*- coding: utf-8 -*-

from django.utils.translation import ugettext as _

from rest_framework import serializers, viewsets, exceptions

from app.courses.models import Course
from app.choosing.models import ResolvedCombination

class TeacherViewObject(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name


class TeacherViewSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class CourseTeachersSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    acronym = serializers.CharField()
    teachers = serializers.SerializerMethodField('_teachers_list')

    def _teachers_list(self, instance):
        # whoops... missing choosing, TODO
        combs = ResolvedCombination.objects.filter(
            course=instance.id
        )

        passed_teachers = list()
        for c in combs.filter(accepted=True):
            passed_teachers.append(c.teacher)

        denied_teachers = list()
        for c in combs.filter(accepted=False):
            denied_teachers.append(c.teacher.id)

        if len(passed_teachers) == 0:
            passed_teachers = instance.teachers.exclude(id__in=denied_teachers)

        teachers = []
        for t in passed_teachers:
            tv = TeacherViewObject(id=t.id, name=str(t))
            tvs = TeacherViewSerializer(tv)
            teachers.append ( tvs.data )
        return teachers

    class Meta:
        model = Course
        fields = ("id", "acronym", "teachers")


class CourseTeachersViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseTeachersSerializer


views_to_register = (
    (r'course-teachers', CourseTeachersViewSet),
)

