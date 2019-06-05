# /StudX_dir/StudX/configuration/tests.py

from django.test import TestCase
from common.utils import *
import xlsxwriter

# Create your tests here.

class TemplateTestCase(TestCase):

	def write_template(self):
		print('testTemplate')
		workbook = xlsxwriter.Workbook('Schedule.xlsx')
		slots = workbook.add_worksheet('Slots')
		teacher = workbook.add_worksheet('Teacher')
		WeekDays = workbook.add_worksheet('WeekDays')

		for cnt, days in enumerate(DAYS_OF_THE_WEEK,1):
		  WeekDays.write('A{}'.format(cnt),days[1])
			   

		WeekDays.data_validation('A:A', {
			'validate': 'list',
			'source': '=WeekDays!$B:$B',
			})
		
		workbook.close()