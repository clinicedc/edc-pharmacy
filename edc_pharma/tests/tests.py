# from django.test import TestCase
# 
# from .forms import DispenseForm
# from django import forms
# from .models import Dispense
# 
# 
# class SmokeTest(TestCase):
#     def test_bad_maths(self):
#         self.assertEqual(1 + 1, 3)
# 
# 
# class TestFormFields(TestCase):
#     def setUp(self):
#         self.subject_identifier = forms.CharField(label='Patient Identifier',
#         max_length=36)
# 
#     def test_forms(self):
#         test_model = Dispense.objects.create()
#         self.assertIsNotNone(test_model.pk)
#         
# # 
# #         form_data = {'initials': 'KK'}
# #         form = Dispense(patient=form_data)
# #         self.assertTrue(form.is_valid())
