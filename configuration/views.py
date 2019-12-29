# /StudX_dir/StudX/configuration/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _
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
import xlsxwriter

# Apps imports
from common.utils import *

# import models
from user.models import User
from configuration.models import Classes

# *** Code start here ***

def generate_teacher_template(request):
	workbook = xlsxwriter.Workbook('teacher.xlsx')
	teacher_sheet = workbook.add_worksheet('teacher')
	
	teacher = User.objects.filter(groups=3)
	print(teacher)
	
	for cnt, item in enumerate(teacher,1):
	  teacher_sheet.write('A{}'.format(cnt),item.username)

	workbook.close()
	return redirect('configuration:init_with_file')

# @login_required
# def download_template(request, type):
	# path = doc_obj.document_file.path
	# file_path = os.path.join(settings.MEDIA_ROOT, path)
	# if os.path.exists(file_path):
		# with open(file_path, 'rb') as fh:
			# response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
			# response['Content-Disposition'] = 'inline; filename=' + \
			# os.path.basename(file_path)
			# return response

def classes_list(request):
	classes_obj_list = Classes.objects.all()
	
	variables = {
		'classes_obj_list': classes_obj_list, 
	}
	
	template = 'configuration/classes_list.html'
	
	return render(request, template, variables)


def init_with_file(request):

	variables = {}
	
	template = 'configuration/init_file_form.html'
	
	return render(request, template, variables)
	