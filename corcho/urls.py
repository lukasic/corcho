# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.contrib import admin

import django.contrib.auth.views as auth_views
import frontend.views as frontend_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^logout/?$', auth_views.logout, {'next_page': '/login'}),
    url(r'^login/?$', auth_views.login, {'template_name': 'login.html', }),
    url(r'^dashboard/?$', frontend_views.dashboard),
    url(r'^courses/?$', frontend_views.courses),
]
