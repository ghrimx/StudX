# /StudX_dir/StudX/student/models.py

# System imports
from django.db import models
from django.conf import settings
from datetime import datetime, date, time, timedelta
from django.utils.translation import gettext as _ # for internationalization
from django.utils import timezone
from django.contrib.auth.models import User
from tinymce import HTMLField
import uuid

# Apps imports
from common.utils import *

# Models imports
from user.models import User
from configuration.models import Classes

class StudentManager(models.Manager):
    def get_queryset(self):
        return super(StudentManager, self).get_queryset().filter(status=1)

class Student(models.Model):
	__tablename__ = 'Student'

	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	matricule = models.CharField(max_length=10, unique=True) # Personal number
	fname = models.CharField(_('First name'),max_length=45, null=False) # First name
	lname = models.CharField(_('Last name'),max_length=45, null=False) # Last name
	status = models.IntegerField(choices=STUDENT_STATUS, default=ACTIVE)
	bday = models.DateField(_('Birthday'), null=False) # Birthday
	country_of_birth = models.CharField(max_length=3, choices=COUNTRIES, blank=True, null=True)
	gender = models.IntegerField(choices=GENDER, default=EMPTY, null=True) # Gender 'M' for male or 'F' for female
	picture = models.ImageField(upload_to='%Y/Profile/', verbose_name=_('Picture'), 
		null=True, 
		blank=True, 
		width_field = 'width_field', 
		height_field = 'height_field') # Location of the student's picture
	height_field = models.IntegerField(default=0)
	width_field = models.IntegerField(default=0)
	start_date = models.DateField(auto_now=True, null=True)
	end_date = models.DateField(default='1000-01-01', null=True)
	ICE_details = HTMLField('Emergency infos', null=True, blank=True) # "in case of ermegency" information
	classe = models.ForeignKey(to='configuration.Classes', related_name='student_classe', on_delete=models.SET_NULL, null=True, blank=True)
	address = models.ForeignKey(to='Address', related_name='student_address', on_delete=models.SET_NULL, null=True, blank=True)
	parent= models.ManyToManyField(to='Parents', through='Relationship' , related_name='student_parent', blank=True)
	comment = models.TextField(max_length=255, null=True, blank=True) # Free text
	created_at = models.DateTimeField(editable=False, auto_now_add=True, auto_now=False, null=True, blank=True) # Creation TIMESTAMP
	updated_at = models.DateTimeField(editable=False, auto_now_add=False, auto_now=True, null=True, blank=True) # Last update TIMESTAMP
	creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='student_created_by', null=True) # Creator username
	last_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='student_updated_by', null=True, blank=True) # Last user username
	

	# get all student having an active status
	objects = StudentManager()
	
	def __str__(self):
		return '{}, {} ({})'.format(self.fname, self.lname, self.matricule)
		
	def get_age(self):
		age = date.today() - self.bday
		age = age.days / 365.2425
		return int(age)
	
	class Meta:
		verbose_name = _('Student')
		verbose_name_plural = _('Students')
		
		
# Define Child - Guardian relationship
# Can be Mother, Father, etc.		
class Relationship(models.Model):
	__tablename__ = 'Relationship'
	
	student = models.ForeignKey(to='Student', on_delete=models.CASCADE, related_name='student_membership', null=True, blank=True)
	parent = models.ForeignKey(to='Parents', on_delete=models.CASCADE, related_name='parent_membership', null=True, blank=True)
	relation = models.IntegerField(choices=RELATIONSHIP, default=EMPTY, null=True, blank=True)
	is_ICE = models.BooleanField(default=True)
	is_InCharge = models.BooleanField(default=False)
	
	def __str__(self):
		return '{0} {1} - {2} {3}'.format(self.student.fname, self.student.lname, self.parent.fname, self.parent.lname)
	
	class Meta:
				ordering = ('is_ICE','is_InCharge')
		
class Parents(models.Model):
	__tablename__ = 'Parents'

	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	fname = models.CharField(_('First name'),max_length=45, null=False) # First name
	lname = models.CharField(_('Last name'),max_length=45, null=False) # Last name
	status = models.IntegerField(choices=STATUS, default=ACTIVE)
	bday = models.DateField(_('Birthday'), null=True) # Birthday
	gender = models.IntegerField(choices=GENDER, default=EMPTY, null=True) # Gender 'M' for male or 'F' for female
	address = models.ForeignKey(to='Address', related_name='parent_address', on_delete=models.SET_NULL, null=True, blank=True)
	
	comment = models.CharField(max_length=255, null=True, blank=True) # Free text
	created_at = models.DateTimeField(editable=False, auto_now_add=True, auto_now=False, null=True, blank=True) # Creation TIMESTAMP
	updated_at = models.DateTimeField(editable=False, auto_now_add=False, auto_now=True, null=True, blank=True) # Last update TIMESTAMP
	creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='parent_created_by', on_delete=models.SET_NULL, null=True) # Creator username
	last_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='parent_updated_by', on_delete=models.SET_NULL, null=True, blank=True) # Last user username
	
	def __str__(self):
		return '{}, {}'.format(self.fname, self.lname)
		
	class Meta:
		verbose_name = _('Parent')
		verbose_name_plural = _('Parents')	

class Parent_hasContacts(models.Model):
	__tablename__ = 'Parent_hasContacts'
	
	parent = models.ForeignKey(to='Parents', related_name='parent_hascontact', on_delete=models.CASCADE)
	contact = models.CharField(_('contact'), max_length=255, null=True)
	type = models.IntegerField(choices=CONTACT_TYPE, null=True)
	comment = models.CharField(max_length=255, null=True, blank=True) # Free text
	created_at = models.DateTimeField(editable=False, auto_now_add=True, auto_now=False, null=True, blank=True) # Creation TIMESTAMP
	updated_at = models.DateTimeField(editable=False, auto_now_add=False, auto_now=True, null=True, blank=True) # Last update TIMESTAMP
	creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='parentcontact_created_by', null=True) # Creator username
	last_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='parentcontact_updated_by', null=True, blank=True) # Last user username
	
	def __str__(self):
		return '{0}-{1}'.format(self.type, self.contact)
	
	class Meta:
		ordering = ('type',)
		verbose_name = _("Parent's contact")
		verbose_name_plural = _("Parent's contacts")
		
class Student_hasContacts(models.Model):
	__tablename__ = 'Student_hasContacts'
	
	student = models.ForeignKey(Student, related_name='student_hascontact' ,on_delete=models.CASCADE)
	contact = models.CharField(_('contact'), max_length=255, null=True)
	type = models.IntegerField(choices=CONTACT_TYPE, null=True)
	
	comment = models.CharField(max_length=255, null=True, blank=True) # Free text
	created_at = models.DateTimeField(editable=False, auto_now_add=True, auto_now=False, null=True, blank=True) # Creation TIMESTAMP
	updated_at = models.DateTimeField(editable=False, auto_now_add=False, auto_now=True, null=True, blank=True) # Last update TIMESTAMP
	creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='studentcontact_created_by', null=True) # Creator username
	last_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='studentcontact_updated_by', null=True, blank=True) # Last user username
	
	def __str__(self):
		return '{0}-{1}'.format(self.type, self.contact)
	
	class Meta:
		verbose_name = _("Student's contact")
		verbose_name_plural = _("Student's contacts")	

def user_directory_path(instance, filename):
    # files are uploaded to MEDIA_ROOT/user_<id>/<filename>
    return '%Y/user_{0}/{1}'.format(instance.student.matricule, filename)
	
class Student_hasDocs(models.Model):
	__tablename__ = 'Student_hasdocs'

	title = models.CharField(_('Title'),max_length=100, null=True, blank=True)
	location = models.FileField(_('Location'),upload_to=user_directory_path, null=True, blank=True)
	description = models.CharField(_('Description'),max_length=255, null=True, blank=True)
	student = models.ForeignKey(Student, on_delete=models.CASCADE)
	
	created_at = models.DateTimeField(editable=False, auto_now_add=True, auto_now=False, null=True, blank=True) # Creation TIMESTAMP
	updated_at = models.DateTimeField(editable=False, auto_now_add=False, auto_now=True, null=True, blank=True) # Last update TIMESTAMP
	creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='studentdoc_created_by', null=True) # Creator username
	last_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='studentdoc_updated_by', null=True, blank=True) # Last user username

	def __str__(self):
		return '{}'.format(self.title)
	
	class Meta:
		verbose_name = _("Student's document")
		verbose_name_plural = _("Student's documents")		

class Address(models.Model):
	__tablename__ = 'Address'
	
	street = models.CharField(_('street'), max_length=255, null=True, blank=True)
	city = models.CharField(_('city'), max_length=255, null=True, blank=True)
	zip = models.IntegerField(_('postal code'), null=True, blank=True)

	class Meta:
		unique_together = ('street', 'city',)
		verbose_name = _("Address")
		verbose_name_plural = _("Addresses")

	def __str__(self):
		return self.street		


		
class Disciplines(models.Model):
	"""
		Misbehaviours are recorded in this table.
		If one or several sanction(s) is/are associated to a misbehaviour the description is in the 'Disciplines_Details' class to handle occurence.
		E.g. a student talked during a lesson. The sanction is to stay after class on Wednesday 18 and Wesneday 28. 
		The description of what is asked to the student to do during these two days is recorder in the 'Disciplines_Details' class. 
	"""
	__tablename__ = 'Disciplines'
	
	type = models.ForeignKey(to='Discipline_type', on_delete=models.SET_NULL, related_name='discipline_type', null=True, blank=True, default=1)
	student = models.ForeignKey(to='Student', on_delete=models.CASCADE, related_name='student_discipline')
	motif = HTMLField(null=True, blank=True)
	fact_date = models.DateField(null=True, blank=True, default=date.today)
	status = models.IntegerField(choices=STATUS, default=ACTIVE, null=True, blank=True)
	issuer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='discipline_issuer', null=True, blank=True) 
	location = models.CharField(max_length=100, null=True, blank=True) 
	comment = models.CharField(max_length=255, null=True, blank=True) # Free text
	created_at = models.DateTimeField(editable=False, auto_now_add=True, auto_now=False, null=True, blank=True) # Creation TIMESTAMP
	updated_at = models.DateTimeField(editable=False, auto_now_add=False, auto_now=True, null=True, blank=True) # Last update TIMESTAMP
	creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='discipline_created_by', null=True) # Creator username
	last_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='discipline_updated_by', null=True, blank=True) # Last user username
	
	def __str__(self):
		return '{0}'.format(self.type)
	
	class Meta:
		ordering = ('-fact_date',)
		verbose_name = _('Discipline')
		verbose_name_plural = _('Disciplines')	

class Disciplines_Details(models.Model):
	__tablename__ = 'Disciplines_details'
	
	discipline = models.ForeignKey(to='Disciplines', on_delete=models.CASCADE, related_name='discipline_detail')
	start_date = models.DateField(null=True, blank=True)
	start_time = models.TimeField(null=True, blank=True)
	finish_date = models.DateField(null=True, blank=True)
	finish_time = models.TimeField(null=True, blank=True)
	description = models.TextField(null=True, blank=True)
	created_at = models.DateTimeField(editable=False, auto_now_add=True, auto_now=False, null=True, blank=True) # Creation TIMESTAMP
	updated_at = models.DateTimeField(editable=False, auto_now_add=False, auto_now=True, null=True, blank=True) # Last update TIMESTAMP
	creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='discipline_detail_created_by', null=True) # Creator username
	last_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='discipline_detail_updated_by', null=True, blank=True) # Last user username
	
	def __str__(self):
		return '{0}'.format(self.id)
		
	class Meta:
		verbose_name = _('Discipline details')
		verbose_name_plural = _('Disciplines details')
		
class Discipline_type(models.Model):
	"""
		- Detention: It requires the pupil to report to a designated area of the school during a specified time on a school day (typically either lunch, or after school) and remain there for a specified period of time
		- In-school suspension: the pupil is not allowed to attend classes for a given period of time
		- Suspension: mandatory leave assigned to a student as a form of punishment that can last anywhere from one day to a few weeks
		- Restorative justice: 
		- Withdrawal of privileges: cell phone,...
		- general interest work
	"""

	__tablename__ = 'Discipline_type'
	
	sanction = models.CharField(_('Sanction'), max_length=100, null=True)
	start_date = models.BooleanField(default=True)
	end_date = models.BooleanField(default=True)
	start_time = models.BooleanField(default=True)
	end_time = models.BooleanField(default=False)
	repeatable = models.BooleanField(default=True)
	alert = models.PositiveSmallIntegerField(default=0)
	description = models.CharField(max_length=255, null=True, blank=True)
	comment = models.CharField(max_length=255, null=True, blank=True) # Free text
	
	def __str__(self):
		return '{0}'.format(self.sanction)
	
	class Meta:
		ordering = ('sanction',)
		verbose_name = _("Discipline's type")
		verbose_name_plural = _("Discipline's types")
		
class Attendances(models.Model):
	__tablename__ = 'Attendances'
	
	student = models.ForeignKey(to='Student', on_delete=models.CASCADE, related_name='student_attendance')
	type = models.IntegerField(choices=ATTENDANCES_TYPE, default=0)
	motif = models.TextField(null=True, blank=True) # REM.: should have been "reason"; redundant with "justification" field
	is_excused = models.BooleanField(default=False)
	justification = models.TextField(null=True, blank=True)
	document = models.ForeignKey(to='Student_hasDocs', on_delete=models.SET_NULL, related_name='document_attendance', null=True, blank=True)
	start_date = models.DateField(null=True, default=date.today)
	start_time = models.TimeField(null=True, blank=True)
	finish_date = models.DateField(null=True, blank=True)
	finish_time = models.TimeField(null=True, blank=True)
	comment = models.CharField(max_length=255, null=True, blank=True) # Free text
	
	created_at = models.DateTimeField(editable=False, auto_now_add=True, auto_now=False, null=True, blank=True) # Creation TIMESTAMP
	updated_at = models.DateTimeField(editable=False, auto_now_add=False, auto_now=True, null=True, blank=True) # Last update TIMESTAMP
	creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='creator_attendance', null=True) # Creator username
	last_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='attendance_updated_by', null=True, blank=True)
	
	def __str__(self):
		return '{0} - {1}'.format(self.student, self.type)
		
	class Meta:
		ordering = ('-start_date','-updated_at',)
		verbose_name = _("Attendance")
		verbose_name_plural = _("Attendances")
		
class Arrivals_Departures(models.Model):
	__tablename__ = 'Arrivals Departures'

	student = models.ForeignKey(to='Student', on_delete=models.CASCADE, related_name='student_arrivals_departures')
	type = models.IntegerField(choices=IN_OUT_TYPE, null=True, blank=True)
	justification = models.TextField(null=True, blank=True) # REM.: should have been "reason"
	document = models.ForeignKey(to='Student_hasDocs', on_delete=models.SET_NULL, related_name='document_arrivals_departures', blank=True, null=True)
	apply_on_date = models.DateField(_('Apply on date'), null=True, default=date.today)
	apply_on_time = models.TimeField(_('Apply on time'), null=True)
	scheduled_time = models.TimeField(_('Scheduled time'), null=True, blank=True)
	time_delta = models.TimeField(null=True, blank=True)
	is_excused = models.BooleanField(default=False)
	comment = models.CharField(max_length=255, null=True, blank=True) # Free text
	
	created_at = models.DateTimeField(editable=False, auto_now_add=True, auto_now=False, null=True, blank=True) # Creation TIMESTAMP
	updated_at = models.DateTimeField(editable=False, auto_now_add=False, auto_now=True, null=True, blank=True) # Last update TIMESTAMP
	creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='creator_arrivals_departures', null=True) # Creator username
	last_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='arrivals_departures_updated_by', null=True, blank=True)
	
	def __str__(self):
		return '{0} - {1}'.format(self.student, self.type)
		
	class Meta:
		ordering = ('-updated_at',)
		verbose_name = _("Arrival Departure")
		verbose_name_plural = _("Arrivals Departures")
		
class Student_Notes(models.Model):
	"""Allow Staff to record various information/remarks/comments about a student.
	   Notes are non public nor private as the head of the school should be able to access them if need be
	"""
	
	__tablename__ = 'Student Notes'

	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	title = models.CharField(max_length=100, null=True, blank=True)
	content = HTMLField(_('Content'), null=True, blank=True)
	note_category = models.ForeignKey(to='Note_Category', related_name='note_category', on_delete=models.SET_NULL, null=True, blank=True)
	student = models.ForeignKey(Student, related_name='student_have_note', on_delete=models.CASCADE, null=False, blank=False)
	
	comment = models.CharField(max_length=255, null=True, blank=True) # Free text
	created_at = models.DateTimeField(editable=False, auto_now_add=True, auto_now=False, null=True, blank=True) # Creation TIMESTAMP
	updated_at = models.DateTimeField(editable=False, auto_now_add=False, auto_now=True, null=True, blank=True) # Last update TIMESTAMP
	creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='creator_student_note') # Creator username
	
	def __str__(self):
		return '{} - {}'.format(self.note_category, self.title)
		
	class Meta:
		ordering = ('-created_at','-updated_at',)
		verbose_name = _('Student Note')
		verbose_name_plural = _('Student Notes')

class Note_Category(models.Model):
	__tablename__ = 'Note category'
	
	name = models.CharField(_('Name'), max_length=45, null=False, blank=True)
	
	def __str__(self):
		return '{}'.format(self.name)
		
	class Meta:
		verbose_name = _("Note's category")
		verbose_name_plural = _("Note's categories")
