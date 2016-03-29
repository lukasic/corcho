# -*- coding: utf-8 -*-

from rest_framework.permissions import BasePermission
from rest_framework import serializers, permissions, exceptions

class ModelSerializerWithModelValidation(serializers.ModelSerializer):

    def validate(self, attrs):
        instance = self.Meta.model(**attrs)
        instance.clean()
        return attrs


class IsStudentUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and hasattr(request.user, 'student')


