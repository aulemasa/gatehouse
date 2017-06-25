#coding: utf-8
from __future__ import unicode_literals, absolute_import, print_function

import datetime

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class VisitData(models.Model):
    visit_date = models.DateField(verbose_name="Data wizyty")
    guest = models.CharField(verbose_name="Imię i nazwisko gościa", max_length=150)
    company = models.CharField(verbose_name="Firma którą reprezentuje", blank=True, max_length=150)
    visit_host = models.CharField(verbose_name="Do kogo", max_length=150)
    plan_hour = models.TimeField(verbose_name="Planowana godzina wizyty",default=datetime.time(00, 00))
    arrive_hour = models.TimeField(verbose_name="Godzina przybycia", null=True, blank=True)
    exit_hour = models.TimeField(verbose_name="Godzina wyjścia", null=True, blank=True)
    coffe = models.NullBooleanField(verbose_name="Kawa")
    lunch = models.NullBooleanField(verbose_name="Lunch")
    comment = models.TextField(verbose_name="Komentarz", max_length=250, blank=True)
    key_in_user = models.ForeignKey(User, verbose_name="Użytkownik")

    def __unicode__(self):
        return unicode("%s: %s %s %s %s" %
                       (self.visit_date, self.guest, self.visit_host, self.plan_hour, self.key_in_user))
