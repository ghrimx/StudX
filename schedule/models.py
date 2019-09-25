# /StudX_dir/StudX/schedule/models.py

# System imports
from django.db import models
from django.conf import settings
from datetime import datetime, date, time, timedelta
from django.utils.translation import gettext as _ # for internationalization
from django.utils import timezone
from django.contrib.auth.models import User

# Apps imports
from common.utils import *

# Models imports
from user.models import User
from configuration.models import *
from student.models import Student

class Schedule(models.Model):
	"""
	This module allows to keep track of student and staff schedule.
	StudX is not a scheduler and another program should be used for this purpose.
	"""
	__tablename__ = 'Schedule'
	
	weekDay = models.IntegerField(choices=DAYS_OF_THE_WEEK)
	startAt = models.TimeField(null=True, blank=True)
	finishtAt = models.TimeField(null=True, blank=True)
	location = models.ForeignKey(to='configuration.Location', on_delete=models.SET_NULL, related_name='schedule_classrooms', null=True, blank=True)
	subject = models.ForeignKey(to='configuration.Subjects', on_delete=models.CASCADE, related_name='schedule_subjects', null=True, blank=True)
	teacher = models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='schedule_teachers') # REM.: should be replaced by 'Staff'
	student = models.ManyToManyField(to='student.Student', related_name='schedule_student', through='Sections', blank=True)
	status = models.IntegerField(choices=SCHEDULE_STATUS, default=ACTIVE)
	comment = models.CharField(max_length=255, null=True, blank=True) # Free text
	updated_at = models.DateTimeField(editable=False, auto_now_add=False, auto_now=True, null=True, blank=True) # Last update TIMESTAMP
	last_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='schedule_updated_by', on_delete=models.SET_NULL, null=True, blank=True) # Last user username
	creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='slots_created_by', on_delete=models.SET_NULL, null=True) # Creator username

	def __str__(self):
		return '{} - {} {} - {}'.format(self.id, self.get_weekDay_display(), self.startAt, self.subject)
		
	class Meta:
		ordering = ('weekDay', 'startAt')
		verbose_name = _('Schedule')
		verbose_name_plural = _('Schedule')
			
class Sections(models.Model):
	'''
	A section is a group of student having the same subject in the same room and at the same time slot of the schedule.
	A section can have student assigned to different "classes".
	Example scenario:
	Classes 1A and 1B have 25 and 10 student respectively. Both classes share common subjects (e.g. Math, science) but have also differents subjects (E.g. 1A has 2hrs of Dutch while 1B has 2hrs of spanish) hence two differents classes.
	However, in order to lower the workload of the teacher having to teach to 25 student at a time, 7 student of classe 1A will have Math with the classe 1B for instance at the same time as the rest of classe 1A has science with another teacher. 
	Two sections are therefore created: one will be 1A1 and the other one will be 1A/1B7 = 1B + 7 student from 1A
	A section allows to accomodate the schedule with maximum of flexibility. 
	It is understood that the content of this table will be of high redundancy with the classe table. 
	'''
	__tablename__ = 'Section'

	section_name = models.CharField(_('Section'), max_length=45)
	student = models.ForeignKey(to='student.Student', on_delete=models.CASCADE, related_name='section_student', null=True, blank=True)
	is_active = models.BooleanField(default=True)
	schedule_slot = models.ForeignKey(to='Schedule', on_delete=models.CASCADE, related_name='slots', null=True, blank=True)
	is_active = models.BooleanField(default=True)

	def __str__(self):
		return '{}'.format(self.section_name)	
	
	class Meta:
		verbose_name = _('Section')
		verbose_name_plural = _('Sections')
