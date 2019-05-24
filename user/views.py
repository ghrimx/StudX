# /StudX_dir/StudX/user/views.py

import random
import string

from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login


# import class from models
from user.models import User, ClasseOwnership
from configuration.models import Classes, Subjects
from django.contrib.auth.models import Group

#import class from forms
from .forms import CustomUserCreationForm, CustomUserChangeForm


def logout_studx(request):
    logout(request)
    request.session.flush()
    return redirect('user:login')

@login_required
def user_list(request):

	user_list = User.objects.all().exclude(is_superuser=True)
	
	variables = {
		'user_list': user_list,
	}
	
	template = 'user/user_list.html'

	return render(request, template, variables)
	
	
@login_required
def create_edit_user(request, user_id=None):
	
	if not request.user.has_perm('user.add_user') and request.user.has_perm('user.edit_user') : 
		return HttpResponseForbidden()

	if user_id:
		user = get_object_or_404(User, id=user_id)
	else:
		user = User()
	
	temp_password = ''.join([random.choice(string.ascii_letters+string.digits+'-_') for ch in range(8)])
	
	if request.method == 'POST':
		if user_id:
			form = CustomUserChangeForm(request.POST, instance=user)
		else: form = CustomUserCreationForm(request.POST, instance=user)
		if form.is_valid():
			user_instance = form.save(commit=False)
			
			if user_id:
				user_instance.password = user.password
			
			user_instance.save()
			
			# assign role to a user
			user.groups.clear()
			for role in form.cleaned_data['groups']:
				group = Group.objects.get(name=role)
				user.groups.add(group)
			
			# assign classes to a user
			user.classe_ownership.clear()
			for classe in form.cleaned_data['classe_ownership']:
				classe = Classes.objects.get(classe_name=classe)
				ClasseOwnership.objects.create(user=user, classe=classe)
				
			# assign subjects to a user
			user.subject.clear()
			print(form.cleaned_data.get('subject'))
			for subject in form.cleaned_data['subject']:
				# subject = Subjects.objects.get(name=subject)
				user.subject.add(subject) 

			return redirect('user:user_list')
		else : 
			print("CustomUserCreationForm is invalid")
			print("errors: ", form.errors)
	else: form = CustomUserCreationForm(instance=user)
	
	variables = {
		'form': form,
		'user': user,
		'temp_password': temp_password,
	}
	
	template = 'user/user_form.html'

	return render(request, template, variables)
	
@login_required
def delete_user(request, user_id):
	if user_id:
		if request.user.has_perm('user.delete_user'):
			user = get_object_or_404(User, pk=user_id)
			user.delete()
			return redirect('user:user_list')
		else: return HttpResponseForbidden()
	else: return Http404()