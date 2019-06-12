# /StudX_dir/StudX/schedule/forms.py

from django import forms
from django.forms.formsets import formset_factory

# import core.models
from django.contrib.auth.models import User
from schedule.models import Schedule

class SlotForm(forms.ModelForm):
	class Meta:
		model = Schedule
		fields =['weekDay', 'startAt', 'finishtAt', 'location', 'subject', 'teacher', 'student', 'status', 'comment']