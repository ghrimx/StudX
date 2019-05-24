# /StudX_dir/StudX/user/forms.py

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.forms.widgets import PasswordInput, TextInput
from user.models import User

class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class':'validate','placeholder': 'Username'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder':'Password'}))
	
class CustomUserCreationForm(UserCreationForm):
	class Meta(UserCreationForm):
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'role', 'is_active', 'groups', 'classe_ownership', 'subject')

class CustomUserChangeForm(UserChangeForm):
	class Meta(UserCreationForm):
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'role', 'is_active', 'groups', 'classe_ownership', 'subject')
		exclude = ('password1','password2',)


