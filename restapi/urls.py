# -*- coding: utf-8 -*-

import datetime

from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework import routers, serializers, viewsets, exceptions

from restapi.api_auth import views_to_register as api_auth_views
from restapi.api_choosing import views_to_register as api_choosing_views

router = routers.DefaultRouter()


def register_views(x):
    for regex, view in x:
        router.register(regex, view)


register_views(api_auth_views)
register_views(api_choosing_views)
