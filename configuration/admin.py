# /StudX_dir/StudX/configuration/admin.py

from django.contrib import admin
from configuration.models import Classes, Subjects, Location, SubjectsSet

# Register your models here.
admin.site.register(Classes)
admin.site.register(Subjects)
admin.site.register(SubjectsSet)
admin.site.register(Location)
