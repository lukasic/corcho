# -*- coding: utf-8 -*-

import datetime

from django.utils.translation import ugettext as _

from rest_framework import serializers, viewsets, exceptions

from app.accounts.models import Student
from app.accounts.helpers import is_student
from app.choosing.models import Choose, Choosing, TeacherRequest
from app.choosing.helpers import get_student_choosings
from app.courses.models import Course

from restapi.common import ModelSerializerWithModelValidation, IsStudentUser


class ChooseSerializer(ModelSerializerWithModelValidation):
    class Meta:
        model = Choose

    phase = serializers.ChoiceField(choices=((0, _('Waiting')),))

    def get_fields(self, *args, **kwargs):
        fields = super(ChooseSerializer, self).get_fields(*args, **kwargs)
        user = self.context['request'].user

        if user.is_superuser:
            return fields

        if user.student:
            course_category_set = list()
            choosing_id_set = list()
            for ch in get_student_choosings(user.student):
                course_category_set.append(ch.course_category)
                choosing_id_set.append(ch.id)
            fields['course'].queryset = Course.objects.filter(category__in=course_category_set)
            fields['choosing'].queryset = Choosing.objects.filter(pk__in=choosing_id_set)

            fields['student'].queryset = Student.objects.filter(user=user)
            return fields

        raise RuntimeError()


class ChooseViewset(viewsets.ModelViewSet):
    queryset = Choose.objects.all()
    serializer_class = ChooseSerializer
    permission_classes = (IsStudentUser,)

    def get_serializer_context(self):
        context = super(ChooseViewset, self).get_serializer_context()
        context['request'] = self.request
        return context

    def get_queryset(self):
        if self.request.user.is_superuser:
            return super(ChooseViewset, self).get_queryset()
        else:
            return Choose.objects.filter(student=self.request.user.student)

    def check_object_permissions(self, request, obj):
        if request.user.is_superuser:
            return
        if not request.user.student:
            raise exceptions.PermissionDenied()
        if request.user.student != obj.student:
            raise exceptions.PermissionDenied()

    def get_object(self):
        obj = super(ChooseViewset, self).get_object()
        self.check_object_permissions(self.request, obj)
        return obj


class TeacherRequestSerializer(serializers.Serializer):
    teacher_id = serializers.IntegerField()
    choose_id = serializers.IntegerField()

    class Meta:
        model = TeacherRequest
        fields = ("choose", "teacher")

    def create(self, validated_data):
        req = TeacherRequest.objects.filter(choose_id=validated_data.get("choose_id"))
        if req:
            req = req[0]
            teacher_id = validated_data.get("teacher_id")

            if req.phase == 1:
                raise Exception(_("Cannot change."))

            if req.phase == 2 and req.teacher_id != teacher_id:
                return TeacherRequest.objects.create(**validated_data)

            req.teacher_id = teacher_id
            req.time = datetime.datetime.now()
            req.save()

        else:
            req = TeacherRequest.objects.create(**validated_data)

        return req


class TeacherRequestViewSet(viewsets.ModelViewSet):
    queryset = TeacherRequest.objects.all()
    serializer_class = TeacherRequestSerializer


views_to_register = (
    (r'choose', ChooseViewset),
    (r'teacher-request', TeacherRequestViewSet),
)


