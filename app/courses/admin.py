# -*- coding: utf-8 -*-

from django.contrib import admin
from django import forms
from import_export.admin import ImportExportActionModelAdmin

from app.courses.models import SubjectClass, CourseCategory, Course


class CourseCategoryAdminForm(forms.ModelForm):
    """
    Be caferul! Relation Course.category -> couse_set is just ForeignKey, not ManyToMany.
    """
    course_set = forms.ModelMultipleChoiceField(
        Course.objects.all(),
        widget=admin.widgets.FilteredSelectMultiple('course_set', False),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(CourseCategoryAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.initial['course_set'] = self.instance.course_set.values_list('pk', flat=True)

    def save(self, *args, **kwargs):
        instance = super(CourseCategoryAdminForm, self).save(*args, **kwargs)
        if instance.pk:
            #instance.course_set.clear()
            instance.course_set.add(*self.cleaned_data['course_set'])
        return instance


class SubjectClassAdmin(ImportExportActionModelAdmin):
    list_display = ("acronym", "name")
    filter_horizontal = ('teachers',)

class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ("acronym", "name", "description")
    form = CourseCategoryAdminForm


class CourseAdmin(ImportExportActionModelAdmin):
    list_display = ("acronym", "name", "category", "subject_class")
    list_filter = ("category", "subject_class")
    list_editable = ("subject_class",)
    filter_horizontal = ("teachers",)


admin.site.register(SubjectClass, SubjectClassAdmin)
admin.site.register(CourseCategory, CourseCategoryAdmin)
admin.site.register(Course, CourseAdmin)
