#coding: utf-8
from __future__ import unicode_literals, absolute_import, print_function

from django import forms

from .models import VisitData

#from django.contrib.auth.models import User

forms.DateInput.input_type="date"
forms.DateInput.input_formats="'%Y-%m-%d'"
forms.DateTimeInput.input_type="datetime-local"
forms.TimeInput.input_type="time"


class VisitCreateForm(forms.ModelForm):

    class Meta:
        model = VisitData
        exclude = ['arrive_hour', 'exit_hour', 'key_in_user']


