# /StudX_dir/StudX/user/utils.py

from django.utils.translation import gettext as _ # for internationalization

ADMIN = 1
SUPERVISOR = 2
SECRETARY = 3
TEACHER = 4
STUDENT = 9

ROLE_CHOICES = (
	(STUDENT, _('student')),
	(TEACHER, _('teacher')),
	(SECRETARY, _('secretary')),
	(SUPERVISOR, _('supervisor')),
	(ADMIN, _('admin')),
	)