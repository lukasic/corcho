# -*- coding: utf-8 -*-

from rest_framework import serializers, viewsets

from django.contrib.auth.models import User
from restapi.common import SuperUserOnly

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

class ListUsers(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (SuperUserOnly,)


views_to_register = (
	(r'users', ListUsers),
)

