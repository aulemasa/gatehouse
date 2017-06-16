#coding: utf-8
from __future__ import unicode_literals, absolute_import, print_function

import django_filters

from .models import VisitData

class DataFilter(django_filters.FilterSet):
    class Meta:
        model = VisitData
        fields = ['visit_date',]
