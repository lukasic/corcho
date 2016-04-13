# -*- coding: utf-8 -*-

from app.choosing.models import Choose, ResolvedCourse, TeacherRequest, ResolvedCombination

from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

@receiver(post_save, sender=ResolvedCourse)
def deny_course_teachers(sender, instance, *args, **kwargs):
	if instance.accepted == True:
		return

	combs = ResolvedCombination.objects.filter(
		choosing=instance.choosing,
		course=instance.course
	)

	for c in combs.all():
		c.delete()

	teachers = instance.course.teachers
	for teacher in teachers.all():
		c = ResolvedCombination()
		c.choosing = instance.choosing
		c.course = instance.course
		c.teacher = teacher
		c.accepted = False
		c.save()

@receiver(post_delete, sender=ResolvedCourse)
def undeny_course_teachers(sender, instance, *args, **kwargs):
	combs = ResolvedCombination.objects.filter(
		choosing=instance.choosing,
		course=instance.course
	)

	for c in combs.all():
		c.delete()


@receiver(post_save, sender=ResolvedCourse)
def resolve_course_chooses(sender, instance, *args, **kwargs):
	chooses = Choose.objects.filter(
		choosing=instance.choosing,
		course=instance.course
	)

	resolution = 0
	if instance.accepted:
		# hope there won't be conflicts
		resolution = 1
	else:
		resolution = 2

	for choose in chooses.all():
		choose.phase = resolution
		choose.save()


@receiver(post_delete, sender=ResolvedCourse)
def unresolve_course_chooses(sender, instance, *args, **kwargs):
	chooses = Choose.objects.filter(
		choosing=instance.choosing,
		course=instance.course
	)

	for choose in chooses.all():
		choose.phase = 0
		choose.save()


@receiver(post_save, sender=Choose)
def post_save_choose(sender, instance, *args, **kwargs):
	resolution = 0
	if instance.phase == 2:
		resolution = 2

	requests = instance.teacherrequest_set
	for request in requests.all():
		request.phase = resolution
		request.save()


@receiver(post_save, sender=ResolvedCombination)
def resolve_teacher_requests(sender, instance, *args, **kwargs):
	reqs = TeacherRequest.objects.filter(
		choose__choosing=instance.choosing,
		choose__course=instance.course,
		teacher=instance.teacher)

	resolution = 0
	if instance.accepted:
		# we don't know yet, if it's accepted!
		#resolution = 1
		pass
	else:
		resolution = 2

	for req in reqs.all():
		req.phase = resolution
		req.save()


@receiver(post_delete, sender=ResolvedCombination)
def unresolve_teacher_requests(sender, instance, *args, **kwargs):
	reqs = TeacherRequest.objects.filter(
		choose__choosing=instance.choosing,
		choose__course=instance.course,
		teacher=instance.teacher)

	for req in reqs.all():
		req.phase = 0
		req.save()

