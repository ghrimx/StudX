# /StudX_dir/StudX/schedule/urls.py

from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from schedule import views

app_name = 'schedule'

urlpatterns = [
	path('schedule/', views.schedule_main, name='schedule_main'),
	path('new/', views.create_edit_slot, name='create_slot'),
	path('slot/<int:id>/edit/', views.create_edit_slot, name='edit_slot'),
	] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)