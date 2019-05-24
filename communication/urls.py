# /StudX_dir/StudX/communication/urls.py

from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from communication import views

app_name = 'communication'

urlpatterns = [
	path('memos/', views.memos_list, name='memos_list'),
	path('memos/create/', views.create_edit_memo, name='create_memo'),
	path('memos/<uuid:memo_uuid>/edit/', views.create_edit_memo, name='edit_memo'),
	path('memos/<uuid:memo_uuid>/delete/', views.delete_memo, name='delete_memo'),
	] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)