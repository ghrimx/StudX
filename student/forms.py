# /StudX_dir/StudX/student/forms.py #

from django import forms
from django.forms.formsets import formset_factory
from tinymce import TinyMCE

# import core.models
from django.contrib.auth.models import User
from student.models import Disciplines, Discipline_type, Disciplines_Details, Arrivals_Departures, Attendances, Student_Notes


# *** Code start here ***
		
class DisciplineForm(forms.ModelForm):
	class Meta:
		model = Disciplines
		# template_name = "core/discipline_form.html"
		fields = ['type','fact_date' , 'student', 'status', 'issuer', 'location', 'motif', 'comment']
		

		
class DisciplineDetailsForm(forms.ModelForm):
	class Meta:
		model = Disciplines_Details
		fields = [
			'start_date',
			'start_time',
			'finish_date',
			'finish_time',
			'description'
		]
		
		widgets = {
			'description': forms.Textarea(attrs={'rows': 1}),
		}
		
DisciplineDetailsFormSet = formset_factory(DisciplineDetailsForm, extra=0)

DisciplineDetailsInlineFormSet = forms.inlineformset_factory(Disciplines, Disciplines_Details, fields = ('id','start_date','start_time','finish_date','finish_time','description'), extra=1)

class inoutForm(forms.ModelForm):
	class Meta:
		model = Arrivals_Departures
		fields = (
			'student',
			'justification',
			'document',
			'apply_on_date',
			'apply_on_time',
			'scheduled_time',
			'time_delta',
			'is_excused',
			'comment'
			)

class StudentNoteForm(forms.ModelForm):
	class Meta:
		model = Student_Notes
		fields = (
			'title',
			'content',
			'note_category',
			)