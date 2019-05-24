# /StudX_dir/StudX/communication/models.py

# import modules
import os
import sys
import uuid

# import django modules
from django.conf import settings
from django.utils.translation import gettext as _ # for internationalization
from django.utils import timezone
from tinymce import HTMLField
from datetime import datetime, date, time, timedelta

# Models
from django.db import models
from django.contrib.auth.models import User
from student.models import Student

# Create your models here.

class Memos(models.Model):
	__tablename__ = 'Memos'

	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	title = models.CharField(max_length=100, null=True, blank=True)
	content = HTMLField('Content', null=True, blank=True)

	comment = models.CharField(max_length=255, null=True, blank=True) # Free text
	created_at = models.DateTimeField(editable=False, auto_now_add=True, auto_now=False, null=True, blank=True) # Creation TIMESTAMP
	updated_at = models.DateTimeField(editable=False, auto_now_add=False, auto_now=True, null=True, blank=True) # Last update TIMESTAMP
	creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='creator_memo') # Creator username
	
	def __str__(self):
		return '{}'.format(self.title)
		
	class Meta:
		ordering = ('-created_at','-updated_at',)
		verbose_name = _('Memo')
		verbose_name_plural = _('Memos')
