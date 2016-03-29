# -*- coding: utf-8 -*-

from django.utils.translation import ugettext as _

from rest_framework import serializers, viewsets, exceptions

from app.accounts.models import Student
from app.accounts.helpers import is_student
from app.choosing.models import Choose, Choosing
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


views_to_register = (
    (r'choose', ChooseViewset),
)


