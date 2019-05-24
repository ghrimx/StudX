# /StudX_dir/StudX/communication/views.py

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

# import models
from communication.models import Memos
from user.models import User

# import forms
from communication.forms import MemoForm

# *** Code start here ***

@login_required()
def memos_list(request):
	memos_obj_list = Memos.objects.all()
	memos_creator_list = User.objects.all()
	
	memo_title_filter = request.POST.get('title')
	memo_creator_filter = request.POST.get('memo_creator')

	# Setup of the form filter id="memo_list_filter" in intercom/templates/memo_list.html 
	if memo_title_filter:
		memos_obj_list = memos_obj_list.filter(title__icontains=memo_title_filter)
	if memo_creator_filter:
		memos_obj_list = memos_obj_list.filter(creator=memo_creator_filter)
	
	variables = {
		'memos_obj_list':memos_obj_list,
		'memos_creator_list':memos_creator_list,
	}
	
	template = 'communication/memos/memos_list.html'
	
	return render(request, template, variables)
	
def create_edit_memo(request, memo_uuid=None):
	if memo_uuid:
		memo_object = get_object_or_404(Memos, uuid=memo_uuid)
		if memo_object.creator != request.user:
			return HttpResponseForbidden()
	else:
		memo_object = Memos(creator=request.user)
	
	if request.POST:
		form = MemoForm(request.POST, instance=memo_object)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('communication:memos_list'))
	else: form = MemoForm(instance=memo_object)

	variables = {
		'form': form,
		'memo_object': memo_object
	}
	
	template = 'communication/memos/memo_form.html'
	
	return render(request, template, variables)

@login_required
def delete_memo(request, memo_uuid):
	if memo_uuid:
		memo_object = get_object_or_404(Memos, pk=memo_uuid)
		if memo_object.creator == request.user:
			memo_object.delete()
			return redirect('communication:memos_list')
		else: return HttpResponseForbidden()
	else: return Http404()