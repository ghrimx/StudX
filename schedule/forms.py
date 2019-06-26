# /StudX_dir/StudX/schedule/forms.py

from django import forms
from django.forms.models import ModelForm
from django.forms.widgets import CheckboxSelectMultiple
from django.forms.formsets import formset_factory

# import core.models
from django.contrib.auth.models import User
from schedule.models import Schedule
from student.models import Student

class SlotForm(forms.ModelForm):
	class Meta:
		model = Schedule
		fields =['weekDay', 'startAt', 'finishtAt', 'location', 'subject', 'teacher', 'student', 'status', 'comment']
		
	def __init__(self, *args, **kwargs):
		super(SlotForm, self).__init__(*args, **kwargs)
		self.fields["student"].widget = CheckboxSelectMultiple()
		self.fields["student"].queryset = Student.objects.select_related('classe').order_by('classe')