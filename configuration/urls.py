# /StudX_dir/StudX/configuration/urls.py

from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url
from django.contrib.auth import views as auth_views

from configuration import views as  config_views
from schedule import views as schedule_views

app_name = 'configuration'

urlpatterns = [
	path('config', config_views.init_with_file, name='init_with_file'),
	path('download', config_views.generate_teacher_template, name='generate_teacher_template'),
	path('classes_list',config_views.classes_list, name='classes_list'),
	path('schedule/<slug:param>',schedule_views.schedule_main, name='getSchedule'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)