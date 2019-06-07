# /StudX_dir/StudX/schedule/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.contrib.auth import logout, authenticate, login
from django.core.paginator import Paginator
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from datetime import datetime, timedelta
from django.db.models import Count

# Apps imports
from common.utils import *

# import models
from schedule.models import Schedule
from configuration.models import Classes
from student.models import Student
from user.models import User

#import forms
from schedule.forms import SlotForm

# *** Code start here ***

@login_required
def schedule_main(request):

	classes = Classes.objects.all()
	schedule = Schedule.objects.none()
	
	classes_filter = request.POST.get('classe')
	
	if classes_filter:
		schedule = Schedule.objects.filter(student__classe=classes_filter)
		for i in range(1,8):
			schedule_list[i] = schedule.filter(weekDay=i)
		print('schedule: ', schedule_list)
	
	variables = {
		'days':DAYS_OF_THE_WEEK,
		'schedule_list':schedule_list,
		'classes':classes, 
	}
	
	template = 'schedule/schedule_main.html'
	
	return render(request, template, variables)
	
@login_required
def create_edit_slot(request, id=None):
	
	if not request.user.has_perm('schedule.add_user') and request.user.has_perm('schedule.edit_schedule') : 
		return HttpResponseForbidden()

	user = request.user

	if id:
		slot = get_object_or_404(Schedule, id=id)
		if discipline.creator != request.user:
			return HttpResponseForbidden()
	else:
		slot = Schedule(creator=user)
	
	classes = Classes.objects.all()
	
	if request.method == 'POST':
		form = SlotForm(request.POST, instance=slot)
		if form.is_valid():
			slot_instance = form.save(commit=False)
			
			if id:
				slot_instance.last_user = user
			
			schedule.teacher.clear()
			for teacher in form.cleaned_data['teacher']:
				schedule.teacher.add(teacher)
			
			schedule.student.clear()
			for student in form.cleaned_data['student']:
				schedule.student.add(student)
				
			slot_instance.save()
		else: 
			print('SlotForm is invalid')
			print('errors: ', form.errors)
	else:
		form = SlotForm(instance=slot)
	
	variables = {
		'classes': classes,
		'form': form,
	}
	
	template = 'schedule/slot_form.html'

	return render(request, template, variables)
		
		
		
		

	
