# -*- coding: utf-8 -*-

from app.choosing.models import TeacherRequest, DeniedCombination

from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete


@receiver(post_save, sender=DeniedCombination)
def deny_teacher_requests(sender, instance, *args, **kwargs):
	reqs = TeacherRequest.objects.filter(
		choose__choosing=instance.choosing,
		choose__course=instance.course,
		teacher=instance.teacher,
		phase=0)

	for req in reqs.all():
		req.phase = 2
		req.save()


@receiver(post_delete, sender=DeniedCombination)
def undeny_teacher_requests(sender, instance, *args, **kwargs):
	reqs = TeacherRequest.objects.filter(
		choose__choosing=instance.choosing,
		choose__course=instance.course,
		teacher=instance.teacher,
		phase=2)

	for req in reqs.all():
		req.phase = 0
		req.save()

