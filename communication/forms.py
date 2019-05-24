# /devdev/StudX_dir/StudX/communication/forms.py

from django import forms

# import communication.models
from communication.models import Memos
from user.models import User

# *** Code start here ***

class MemoForm(forms.ModelForm):
	class Meta:
		model = Memos
		template_name = "communication/memos/memo_form.html"
		fields = ['title', 'content']