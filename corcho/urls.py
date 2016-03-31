# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from django.contrib import admin

import django.contrib.auth.views as auth_views

import frontend.views as frontend_views
import frontend.views_student as frontend_views_student

from restapi.urls import router as restapi_router

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(restapi_router.urls, namespace='api')),
    url(r'^logout/?$', auth_views.logout, {'next_page': '/login'}),
    url(r'^login/?$', auth_views.login, {'template_name': 'login.html', }),
    url(r'^dashboard/?$', frontend_views.dashboard),
    url(r'^courses/?$', frontend_views.courses),
    url(r'^student/choosing/?$', frontend_views_student.phase2_choosing),
    url(r'^student/courses/?$', frontend_views_student.my_courses),
    url(r'^student/teachers-requests/?$', frontend_views_student.teachers_requests),
]
