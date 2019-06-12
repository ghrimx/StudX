# /StudX_dir/StudX/user/models.py

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext as _ # for internationalization

from configuration.models import Classes, Subjects
from user.utils import ROLE_CHOICES

# Create your models here.

class User(AbstractUser):
	__tablename__ = 'User'

	role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, null=True, blank=True)
	classe_ownership = models.ManyToManyField(to='configuration.Classes', related_name='owner_classe', through='ClasseOwnership', blank=True)
	subject = models.ManyToManyField(to='configuration.Subjects', related_name='subjects_taught', blank=True)
	
	def __str__(self):
		return '{}'.format(self.username)

class ClasseOwnership(models.Model):
	__tablename__ = 'Classe Ownership'
	
	user = models.ForeignKey(to='User', on_delete=models.CASCADE, related_name='+')
	classe = models.ForeignKey(to='configuration.Classes', on_delete=models.CASCADE, related_name='+')

	def __str__(self):
		return '{} - {}'.format(self.user.username, self.classe.classe_name)

