# -*- coding: utf-8 -*-

from django import forms
from django.contrib import admin
from django.utils.translation import gettext as _

from app.choosing.models import Choosing, Choose, TeacherRequest, ResolvedCourse, ResolvedCombination
from app.courses.models import Course


class ChoosingAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ChoosingAdminForm, self).__init__(*args, **kwargs)

        if self.instance.id:
            self.fields['denied_courses'].queryset = self.instance.course_category.course_set.all()


class ChoosingAdmin(admin.ModelAdmin):
    list_display = ("acronym", "name", "course_category", "phase", "time_start", "time_end", "active", "priority", "allow_teacher_requests")
    list_filter = ("course_category", "phase", "active")
    fieldsets = (
        ( '', { 'fields': ('acronym', 'name', 'course_category') }, ),
        ( _('Control'), { 'fields': ('time_start', 'time_end', 'active', 'priority', 'phase', 'for_grade', 'courses_min', 'courses_max', "allow_teacher_requests") } ),
        ( _('Phase: Changes in choosings'), { 'fields': ('denied_courses',) })
    )
    filter_horizontal = ["denied_courses",]
    form = ChoosingAdminForm

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields
        return self.readonly_fields + ("denied_courses",)


class ChooseAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "choosing", "phase", "created_at")
    list_filter = ("student", "course", "choosing", "phase")
    search_fields = ("student__user__username", "course__name", "choosing__name", "phase")

    def get_readonly_fields(self, request, obj=None):
        ro_fields = self.readonly_fields or list()
        if obj:
            ro_fields.append("student")
            ro_fields.append("course")
            ro_fields.append("choosing")
        return ro_fields


class TeacherRequestAdmin(admin.ModelAdmin):
    list_display = ("choose", "teacher", "phase", "created_at")
    list_filter = ("choose__choosing", "teacher", "phase")
    search_fields = ("choose__student__user__username", "choose__course__name", "teacher__user__username")

    def get_readonly_fields(self, request, obj=None):
        ro_fields = self.readonly_fields or list()
        if obj:
            ro_fields.append("choose")
            ro_fields.append("teacher")
        return ro_fields


class ResolvedCourseAdmin(admin.ModelAdmin):
    list_display = ('choosing', 'course', 'accepted')

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.list_display
        return self.readonly_fields


class ResolvedCombinationAdmin(admin.ModelAdmin):
    list_display = ('choosing', 'course', 'teacher', 'accepted')

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.list_display
        return self.readonly_fields


admin.site.register(Choosing, ChoosingAdmin)
admin.site.register(Choose, ChooseAdmin)
admin.site.register(TeacherRequest, TeacherRequestAdmin)
admin.site.register(ResolvedCourse, ResolvedCourseAdmin)
admin.site.register(ResolvedCombination, ResolvedCombinationAdmin)
