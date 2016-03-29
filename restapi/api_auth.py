# -*- coding: utf-8 -*-

from rest_framework import serializers, viewsets

from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

class ListUsers(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


views_to_register = (
	(r'users', ListUsers),
)

