# /StudX_dir/StudX/student/urls.py

from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from student import views

app_name = 'student'

urlpatterns = [
	path('student_list', views.student_list, name='student_list'),
	path('<uuid:uuid>/details/', views.view_student, name='view_student'),
	path('<uuid:student_uuid>/note/create', views.create_edit_student_note, name='create_student_note'),
	path('<uuid:student_uuid>/note/<uuid:note_uuid>/edit', views.create_edit_student_note, name='edit_student_note'),
	path('<uuid:student_uuid>/note/<uuid:note_uuid>/delete', views.delete_student_note, name='delete_student_note'),
	path('disciplines/', views.disciplines_list, name='disciplines_list'),
	path('<int:id>/details/', views.discipline_details, name='discipline_details'),
	path('discipline/create/', views.create_edit_discipline, name='create_discipline'), 
	path('discipline/<int:id>/edit/', views.create_edit_discipline, name='edit_discipline'), 
	path('discipline/<int:id>/delete/', views.delete_discipline, name='delete_discipline'),
	path('attendances/', views.attendance_list, name='attendance_list'),
	path('<slug:inout_str>/', views.in_out_list, name='in_out_list'),
	path('<slug:inout_str>/<int:id>/details/', views.in_out_details, name='in_out_details'),
	path('<slug:inout_str>/<int:id>/delete/', views.delete_inout, name='delete_inout'),
	path('<slug:inout_str>/create/', views.create_edit_inout, name='create_inout'),
	path('<slug:inout_str>/<int:id>/edit/', views.create_edit_inout, name='edit_inout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)