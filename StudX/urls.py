"""StudX URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

import dashboard.urls, student.urls, user.urls, communication.urls, configuration.urls, schedule.urls


urlpatterns = [
	url(r'^tinymce/', include('tinymce.urls')),
	path('schedule/', include(schedule.urls, namespace='schedule')),
	path('configuration/', include(configuration.urls, namespace='configuration')),
	path('communication/', include(communication.urls, namespace='communication')),
	path('user/', include(user.urls, namespace='user')),
	path('dashboard/', include(dashboard.urls, namespace='dashboard')),
	path('student/', include(student.urls, namespace='student')),
	path('admin/', admin.site.urls),
	]

# Change admin site title
admin.site.site_header = "StudX Administration"
