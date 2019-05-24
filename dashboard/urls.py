# /StudX_dir/StudX/dashboard/urls.py

from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url
from django.contrib.auth import views as auth_views

# import from App
from dashboard import views

app_name = 'dashboard'

urlpatterns = [
	path( '', views.dashboard, name='dashboard'),
	]