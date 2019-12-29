# /StudX_dir/StudX/configuration/urls.py

from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url
from django.contrib.auth import views as auth_views

from configuration import views

app_name = 'configuration'

urlpatterns = [
	path('config', views.init_with_file, name='init_with_file'),
	path('download', views.generate_teacher_template, name='generate_teacher_template'),
	path('classes_list',views.classes_list, name='classes_list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)