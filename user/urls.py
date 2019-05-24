# /StudX_dir/StudX/user/urls.py

from django.urls import path
from django.conf.urls.static import static
from django.conf.urls import url
from user.forms import CustomAuthForm
from django.contrib.auth import views as auth_views

from user import views

app_name = 'user'

urlpatterns = [
	url(r'^logout/$', views.logout_studx, name='logout'),
	path('login/', auth_views.LoginView.as_view(), name='login'),
	path('logout/', auth_views.LogoutView.as_view(), name='Logout'),
	path('list/', views.user_list, name='user_list'),
	path('new/', views.create_edit_user, name='create_user'),
	path('<int:user_id>/edit/', views.create_edit_user, name='edit_user'),
	path('<int:user_id>/delete/', views.delete_user, name='delete_user'),
]