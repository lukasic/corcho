# -*- coding: utf-8 -*-

from django.contrib import admin
from app.accounts.models import Classroom, Student, Teacher


class ClassroomAdmin(admin.ModelAdmin):
	list_display = ('__str__', 'grade', 'name')
	list_filter = ('grade',)


class StudentAdmin(admin.ModelAdmin):
    list_display = ("user", "classroom")
    list_filter = ("classroom",)


class TeacherAdmin(admin.ModelAdmin):
    list_display = ("get_titled_name", )


admin.site.register(Classroom, ClassroomAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher, TeacherAdmin)
