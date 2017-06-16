#coding: utf-8
from __future__ import unicode_literals, absolute_import, print_function

from django import forms

from .models import VisitData
#from django.contrib.auth.models import User
from .models import User
import re
from django.core.exceptions import ObjectDoesNotExist

forms.DateInput.input_type="date"
forms.DateInput.input_formats="'%Y-%m-%d'"
forms.DateTimeInput.input_type="datetime-local"
forms.TimeInput.input_type="time"


class VisitCreateForm(forms.ModelForm):

    class Meta:
        model = VisitData
        exclude = ['arrive_hour','exit_hour','key_in_user']


class RegisterForm(forms.Form):
    username = forms.CharField(label="Login:", max_length=30)
    email = forms.EmailField(label="Email:", required=False)
    password1 = forms.CharField(label="Hasło:", widget=forms.PasswordInput())
    password2 = forms.CharField(label="Powtórz hasło:", widget=forms.PasswordInput())
    first_name = forms.CharField(label="Imię:",max_length=20, required=False)
    last_name = forms.CharField(label="Nazwisko:",max_length=30, required=False)
    log_on = forms.BooleanField(label="Logowanie po rejestracji:", required=False)

    def clean_password2(self):
        password1=self.cleaned_data['password1']
        password2=self.cleaned_data['password2']
        if password1==password2:
            return password2
        else:
            raise forms.ValidationError("Hasła się różnią")

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$',username):
            raise forms.ValidationError("Dopuszczalne są tylko cyfry, litery angielskie i _")
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError("Taki użytkownik już istnieje")


