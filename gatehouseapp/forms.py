# coding: utf-8
from __future__ import unicode_literals, absolute_import, print_function

from django import forms

from .models import VisitData


class VisitCreateForm(forms.ModelForm):

    class Meta:
        model = VisitData
        exclude = ['arrive_hour', 'exit_hour', 'key_in_user']


