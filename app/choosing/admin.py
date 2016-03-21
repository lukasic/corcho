# -*- coding: utf-8 -*-

from django import forms
from django.contrib import admin
from django.utils.translation import gettext as _

from app.choosing.models import Choosing, Choose, TeacherRequest
from app.courses.models import Course


class ChoosingAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ChoosingAdminForm, self).__init__(*args, **kwargs)

        if self.instance.id:
            self.fields['denied_courses'].queryset = self.instance.course_category.course_set.all()


class ChoosingAdmin(admin.ModelAdmin):
    list_display = ("acronym", "name", "course_category", "phase", "time_start", "time_end", "active", "priority")
    list_filter = ("course_category", "phase", "active")
    fieldsets = (
        ( '', { 'fields': ('acronym', 'name', 'course_category') }, ),
        ( _('Control'), { 'fields': ('time_start', 'time_end', 'active', 'priority', 'phase', 'for_grade', 'courses_min', 'courses_max') } ),
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


class TeacherRequestAdmin(admin.ModelAdmin):
    list_display = ("choose", "teacher", "phase", "created_at")
    list_filter = ("choose__choosing", "teacher", "phase")
    search_fields = ("choose__student", "choose__course", "teacher__user__username")


admin.site.register(Choosing, ChoosingAdmin)
admin.site.register(Choose, ChooseAdmin)
admin.site.register(TeacherRequest, TeacherRequestAdmin)
