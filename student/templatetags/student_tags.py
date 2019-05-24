# /StudX_dir/StudX/student/templatetags/student_tags.py

from django import template
register = template.Library()

@register.filter
def verbose_name(obj):
    return obj._meta.verbose_name

@register.filter
def verbose_name_plural(obj):
    return obj._meta.verbose_name_plural
	
@register.filter
def subtract(value, arg):
	return value - arg
	
@register.filter
def get_first_letter(word):
	""" Returns the first character of word in upercase """
	return word[0].upper()
	
@register.filter
def get_status_color(status):
	""" Returns the color of the status """
	status_color = {
		0:"light",
		1:"danger",
		2:"success",
		3:"light"
		}
	return status_color.get(status)