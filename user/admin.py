# /StudX_dir/StudX/user/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from user.models import User

from .forms import CustomUserCreationForm
from .models import User, ClasseOwnership


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(ClasseOwnership)

