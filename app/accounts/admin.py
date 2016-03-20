# -*- coding: utf-8 -*-

from django import forms
from django.contrib import admin
from app.accounts.models import Classroom, Student, Teacher


class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'grade', 'name')
    list_filter = ('grade',)


class StudentAdmin(admin.ModelAdmin):
    list_display = ("user", "classroom")
    list_filter = ("classroom",)


class TeacherSubjectClassAdminForm(forms.ModelForm):
    # Hack - circular dependency
    from app.courses.models import SubjectClass, Course
    subjectclass_set = forms.ModelMultipleChoiceField(
        SubjectClass.objects.all(),
        widget=admin.widgets.FilteredSelectMultiple('subjectclass_set', False),
        required=False,
    )
    course_set = forms.ModelMultipleChoiceField(
        Course.objects.all(),
        widget=admin.widgets.FilteredSelectMultiple('course_set', False),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(TeacherSubjectClassAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.initial['subjectclass_set'] = self.instance.subjectclass_set.values_list('pk', flat=True)
            self.initial['course_set'] = self.instance.course_set.values_list('pk', flat=True)

    def save(self, *args, **kwargs):
        instance = super(TeacherSubjectClassAdminForm, self).save(*args, **kwargs)
        if instance.pk:
            instance.subjectclass_set.clear()
            instance.subjectclass_set.add(*self.cleaned_data['subjectclass_set'])

            instance.course_set.clear()
            instance.course_set.add(*self.cleaned_data['course_set'])
        return instance


class TeacherAdmin(admin.ModelAdmin):
    list_display = ("get_titled_name", 'subjects_list', 'courses_list')
    form = TeacherSubjectClassAdminForm


admin.site.register(Classroom, ClassroomAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher, TeacherAdmin)
