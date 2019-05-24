# /StudX_dir/StudX/student/admin.py

from django.contrib import admin
from .models import Student, Parents, Student_hasContacts, Student_hasDocs, Address, Parent_hasContacts, Relationship, Disciplines, Disciplines_Details, Discipline_type, Attendances, Arrivals_Departures, Student_Notes, Note_Category

# Register your models here.
admin.site.register(Student)
admin.site.register(Parents)
admin.site.register(Student_hasContacts)
admin.site.register(Student_hasDocs)
admin.site.register(Address)
admin.site.register(Parent_hasContacts)
admin.site.register(Relationship)
admin.site.register(Disciplines)
admin.site.register(Disciplines_Details)
admin.site.register(Discipline_type)
admin.site.register(Attendances)
admin.site.register(Arrivals_Departures)
admin.site.register(Student_Notes)
admin.site.register(Note_Category)