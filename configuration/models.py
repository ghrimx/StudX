# /StudX_dir/StudX/configuration/models.py

# System imports
import uuid

# Django imports
from django.db import models
from django.conf import settings
from datetime import datetime, date, time, timedelta
from django.utils.translation import gettext as _ # for internationalization
from django.utils import timezone
from django.contrib.auth.models import User

# Apps imports
from common.utils import *

'''
A "classe" is a group of a given number of student (e.g. max. 25 student per classe) having the same set of subjects.
A classe can have as little as a single student and a maximum number of student decided by the school authority. Classes may share subjects taught by the same teacher. 
Therefore, if the number of student assigned to the same set of subjects outnumbered the maximum per classe, a new one is created and eventually the total number of student is equally distributated between the classes.
'''
class Classes(models.Model):
	__tablename__ = 'Classes'
	
	classe_name = models.CharField(_('classe'), max_length=45, null=True, blank=True)
	subject = models.ManyToManyField(to='Subjects', related_name='classe_subjects', through='SubjectsSet', blank=True)
	is_active = models.BooleanField(default=True)
	
	def __str__(self):
		return '{}'.format(self.classe_name)
	
	class Meta:
		verbose_name = _("Classe")
		verbose_name_plural = _("Classes")		

'''
Classroom
'''		
class Location(models.Model):
	__tablename__='Location'
		
	location = models.CharField(max_length=25, unique=True)
	capacity = models.SmallIntegerField(null=True, blank=True)
	
	def __str__(self):
		return '{}'.format(self.location)	

class SubjectsSet(models.Model):
	__tablename__='SubjectsSet'
	
	subject = models.ForeignKey(to='Subjects', on_delete=models.CASCADE, related_name='+')
	classe = models.ForeignKey(to='Classes', on_delete=models.CASCADE, related_name='+')
	hours = models.IntegerField(null=True, blank=True)
	set = models.CharField(max_length=10, blank=True)	
	
	def __str__(self):
		return '{} - {} - {}'.format(self.subject, self.classe, self.set)	
	
	
class Subjects(models.Model):
	__tablename__='Subjects'
	
	code = models.CharField(max_length=20, unique=True)
	name = models.CharField(max_length=50, blank=True)
	description = models.CharField(max_length=255, null=True, blank=True) # Free text
	
	def __str__(self):
		return '{} - {}'.format(self.code, self.name)	
	
	class Meta:
		verbose_name = _('Subject')
		verbose_name_plural = _('Subjects')
	
