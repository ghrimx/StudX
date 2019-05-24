# /StudX_dir/StudX/student/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import IntegrityError, transaction
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.urls import reverse, reverse_lazy
from django.core.paginator import Paginator
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from datetime import datetime, timedelta
from django.db.models import Count

# import class from models
from student.models import Student, Relationship, Parents, Parent_hasContacts, Student_hasContacts, Student_hasDocs, Address, Discipline_type, Disciplines, Disciplines_Details, Arrivals_Departures, Attendances, Student_Notes
from user.models import User, ClasseOwnership
from configuration.models import Classes

#import class from forms.py
from student.forms import DisciplineForm, DisciplineDetailsForm, DisciplineDetailsFormSet, DisciplineDetailsInlineFormSet, inoutForm, StudentNoteForm

from common import *

# Create your views here.

@login_required
def student_list(request):

	classe_obj_list = ClasseOwnership.objects.filter(user_id=request.user.id).values_list('classe') # get all classes id that the user is accountable for
	classes = Classes.objects.filter(id__in=classe_obj_list) # get classes objects that user is accountable for
	student_obj_list = Student.objects.filter(classe__in=classe_obj_list).order_by('matricule')
	
	student_fname_filter = request.POST.get('fname')
	student_lname_filter = request.POST.get('lname')
	student_classe_filter = request.POST.get('classe')

	
	# Setup of the form filter id="student_list_filter" in core/templates/student.html 
	if student_fname_filter:
		student_obj_list = student_obj_list.filter(fname__icontains=student_fname_filter)
	if student_lname_filter :
		student_obj_list = student_obj_list.filter(lname__icontains=student_lname_filter)
	if student_classe_filter:
		student_obj_list = student_obj_list.filter(classe=student_classe_filter)
	
	variables = {
		'student_obj_list': student_obj_list, 
		'classes':classes, 
	}
	
	template = 'student/student_list.html'
	
	return render(request, template, variables)
	
@login_required
def view_student(request, uuid):
	user = request.user
	student_record = get_object_or_404(Student, uuid=uuid)
	student_contacts = student_record.student_hascontact.all()
	relationship = Relationship.objects.filter(student=student_record).order_by('relation')

	# Discipline
	student_disciplines = student_record.student_discipline.all().order_by('-updated_at')
	student_discipline_stats = student_disciplines.exclude(type_id__isnull=True).values('type__sanction').annotate(num_sanction=Count('type')).order_by('type_id')
	student_disciplines_count = student_disciplines.count()
	student_sanctions_count = student_disciplines.exclude(type_id__isnull=False).count()
	
	# Attendance
	student_attendances = student_record.student_attendance.filter(type=0)
	student_absences_stats = student_attendances.values('is_excused').annotate(num_abscences=Count('is_excused')).order_by()
	student_absences_count = student_attendances.count()
	
	# Arrivals
	student_tardiness = student_record.student_arrivals_departures.filter(type=1)
	student_tardiness_stats = student_tardiness.values('is_excused').annotate(num_tardiness=Count('is_excused')).order_by()
	student_tardiness_count = student_tardiness.count()
	
	# Student Notes
	student_notes = student_record.student_have_note.all()
	
	variables = {
		'student_record': student_record, 
		'student_contacts': student_contacts, 
		'relationship':relationship, 
		'student_disciplines': student_disciplines, 
		'student_discipline_stats':student_discipline_stats, 
		'student_disciplines_count':student_disciplines_count,
		'student_sanctions_count':student_sanctions_count,
		'student_attendances':student_attendances,
		'student_absences_stats':student_absences_stats,
		'student_absences_count':student_absences_count,
		'student_tardiness':student_tardiness,
		'student_tardiness_stats':student_tardiness_stats,
		'student_tardiness_count':student_tardiness_count, 
		'student_notes': student_notes,
	}
	
	template = 'student/student_details/student_details.html'
	
	return render(request, template, variables)
	
@login_required
def disciplines_list(request):
	classe_obj_list = ClasseOwnership.objects.filter(user_id=request.user.id).values_list('classe') # get all classes that the user is accountable for
	student_obj_list = Student.objects.filter(classe__in=classe_obj_list)
	disciplines_obj_list = Disciplines.objects.filter(student__in=student_obj_list)
	disciplines_type_obj_list = Discipline_type.objects.all().only('sanction') # get all discipline types
	
	discipline_type_filter = request.POST.get('sanction')
	student_fname_filter = request.POST.get('fname')
	student_lname_filter = request.POST.get('lname')
	student_classe_filter = request.POST.get('classe')
	fact_date_filter = request.POST.get('fact_date')
	
	# Setup of the form filter id="discipline_list_filter" in student/templates/disciplines.html 
	if discipline_type_filter:
		disciplines_obj_list = disciplines_obj_list.filter(type__id=discipline_type_filter)
	if student_fname_filter:
		disciplines_obj_list = disciplines_obj_list.filter(student__fname__icontains=student_fname_filter)
	if student_lname_filter :
		disciplines_obj_list = disciplines_obj_list.filter(student__lname__icontains=student_lname_filter)
	if student_classe_filter:
		disciplines_obj_list = disciplines_obj_list.filter(student__classe__id=student_classe_filter)
	if fact_date_filter:
		disciplines_obj_list = disciplines_obj_list.filter(fact_date=fact_date_filter)
	
	variables = {
		'disciplines_obj_list': disciplines_obj_list, 
		'classe_obj_list':classe_obj_list, 
		'disciplines_type_obj_list':disciplines_type_obj_list, 
	}
	
	template = 'student/disciplines/disciplines.html'
	
	return render(request, template, variables)

@login_required
def discipline_details(request, id):
	discipline_record = Disciplines.objects.get(pk=id)
	discipline_details = Disciplines_Details.objects.filter(discipline=discipline_record.id)
	discipline_params = Discipline_type.objects.get(pk=discipline_record.type_id)
	
	variables = {
		'discipline_record': discipline_record,
		'discipline_details': discipline_details,
		'discipline_params': discipline_params,
	}
	
	template = 'student/disciplines/discipline_details.html'
	
	return render(request, template, variables)
	
@login_required
def create_edit_discipline(request, id=None):
	"""
		This is an inline formset to create a new discipline entry along with discipline details that can have multiple occurences.
	"""
 
	user = request.user
	
	if id: 
		discipline = get_object_or_404(Disciplines, id=id)
		discipline_details = Disciplines_Details.objects.filter(discipline=discipline)
		formset = DisciplineDetailsInlineFormSet(instance=discipline)
		if discipline.creator != request.user:
			return HttpResponseForbidden()
	else:
		discipline = Disciplines(creator=user)
		formset = DisciplineDetailsInlineFormSet(instance=discipline)
	
	if request.POST:
		form = DisciplineForm(request.POST, instance=discipline)
		formset = DisciplineDetailsInlineFormSet(request.POST,prefix='discipline_detail')
		if form.is_valid():
			discipline_form = form.save(commit=False)
			if id:
				discipline_form.last_user = user
			formset = DisciplineDetailsInlineFormSet(request.POST,prefix='discipline_detail',instance=discipline_form)
			if formset.is_valid():
				discipline_form.save()
				discipline_details = formset.save(commit=False)
				for e in discipline_details:
					if id:
						e.last_user = user
					else: e.creator = user
					e.save()
				return redirect('student:disciplines_list')
			else: 
				print("formset not valid")
				print("error ", formset.errors)
				print("non form error ", formset.non_form_errors())
		else: print("form not valid")
	else:
		form = DisciplineForm(instance=discipline)
		formset = DisciplineDetailsInlineFormSet(instance=discipline)
	
	variables = {
		'form': form,
		'formset': formset
	}
	
	template = 'student/disciplines/discipline_form.html'

	return render(request, template, variables)
	
@login_required
def delete_discipline(request, id):
	if id:
		discipline_object = get_object_or_404(Disciplines, pk=id)
		if discipline_object.creator == request.user:
			discipline_object.delete()
			return redirect('student:disciplines_list')
		else:
			return HttpResponseForbidden()
	else:
		return Http404()

@login_required
def in_out_list(request, inout_str):

	id_type = IN_OUT_TYPE_DICT[inout_str] # get the id (type(id) => integer)
	
	classe_obj_list = ClasseOwnership.objects.filter(user_id=request.user.id).values_list('classe') # get all classes that the user is accountable for
	student_obj_list = Student.objects.filter(classe__in=classe_obj_list).order_by('id')
	in_out_list = Arrivals_Departures.objects.filter(type=id_type).filter(student__in=student_obj_list)
	
	student_fname_filter = request.POST.get('fname')
	student_lname_filter = request.POST.get('lname')
	student_classe_filter = request.POST.get('classe')
	date_filter = request.POST.get('apply_on_date')
	
	if student_fname_filter:
		in_out_list = in_out_list.filter(student__fname__icontains=student_fname_filter)
	if student_lname_filter :
		in_out_list = in_out_list.filter(student__lname__icontains=student_lname_filter)
	if student_classe_filter:
		in_out_list = in_out_list.filter(student__classe__id=student_classe_filter)
	
	variables = {
		'in_out_list': in_out_list, 
	}
	
	template = 'student/arrivals_departures/in_out_list.html'
	
	return render(request, template, variables)		

@login_required
def in_out_details(request, id, inout_str):
	record = get_object_or_404(Arrivals_Departures, pk=id)
	
	variables = {
		'record': record,
	}
	
	template = 'student/arrivals_departures/in_out_details.html'
	
	return render(request, template, variables)
	
@login_required
def create_edit_inout(request, inout_str, id=None):
	'''
		inout_str = 'Arrival' or 'Departure' is passed via the url
		id = record id from the Arrivals_Departures table
		uuid = student uuid from Student table
	'''

	id_type = IN_OUT_TYPE_DICT[inout_str] # get the id (type(id) => integer)
	
	if id:
		inout_object = get_object_or_404(Arrivals_Departures, id=id)
		if not request.user.is_staff and inout_object.creator != request.user :
			return HttpResponseForbidden()
	else:
		inout_object = Arrivals_Departures(creator=request.user)
	
	if request.method == 'POST':
		form = inoutForm(request.POST, instance=inout_object)
		if form.is_valid():
			inout_instance = form.save(commit=False)
			
			# create object
			if not id: 
				inout_instance.type = id_type
			inout_instance.save()
			return redirect('student:in_out_list', inout_str)
		else: 
			print("IN_OUT form is not valid") 
			print("errors:", form.errors)
	else: form = inoutForm(instance=inout_object)
	
	variables = {
		'form': form,
		'inout_object': inout_object,
		'id_type': id_type
	}
	
	template = 'student/arrivals_departures/in_out_form.html'

	return render(request, template, variables)

@login_required
def delete_inout(request, inout_str, id):
	if id:
		inout_object = get_object_or_404(Arrivals_Departures, pk=id)
		if inout_object.creator == request.user:
			inout_object.delete()
			return redirect('student:in_out_list',inout_str)
		else: return HttpResponseForbidden()
	else: return Http404()
			
@login_required
def attendance_list(request):
	classe_obj_list = ClasseOwnership.objects.filter(user_id=request.user.id).values_list('classe') # get all classes that the user is accountable for
	student_obj_list = Student.objects.filter(classe__in=classe_obj_list).order_by('id')
	attendance_list = Attendances.objects.filter(type=0).filter(student__in=student_obj_list)
	
	student_fname_filter = request.POST.get('fname')
	student_lname_filter = request.POST.get('lname')
	student_classe_filter = request.POST.get('classe')
	
	if student_fname_filter:
		in_out_list = in_out_list.filter(student__fname__icontains=student_fname_filter)
	if student_lname_filter :
		in_out_list = in_out_list.filter(student__lname__icontains=student_lname_filter)
	if student_classe_filter:
		in_out_list = in_out_list.filter(student__classe__id=student_classe_filter)
	
	variables = {
		'attendance_list': attendance_list, 
	}
	
	template = 'student/attendances/attendance_list.html'
	
	return render(request, template, variables)	

@login_required	
def create_edit_student_note(request, student_uuid, note_uuid=None):
	if note_uuid:
		note_object = get_object_or_404(Student_Notes, uuid=note_uuid)
		if note_object.creator != request.user:
			return HttpResponseForbidden()
	else:
		note_object = Student_Notes(creator=request.user)
	
	if request.method == 'POST':
		form = StudentNoteForm(request.POST, instance=note_object)
		if form.is_valid():
			note_instance = form.save(commit=False)

			if not note_uuid:
				note_instance.student_id = student_uuid

			note_instance = form.save()

			return redirect('student:view_student', student_uuid)
		else: 
			print("StudentNoteForm is not valid") 
			print("errors:", form.errors)
	else: form = StudentNoteForm(instance=note_object)
	
	variables = {
		'form': form,
		'note_object': note_object,
	}
	
	template = 'student/notes/student_note_form.html'

	return render(request, template, variables)
	
@login_required
def delete_student_note(request, student_uuid, note_uuid):
	if note_uuid:
		note_object = get_object_or_404(Student_Notes, pk=note_uuid)
		if note_object.creator == request.user:
			note_object.delete()
			return redirect('student:view_student', student_uuid)
		else: return HttpResponseForbidden()
	else: return Http404()