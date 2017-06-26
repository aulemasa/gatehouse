#coding: utf-8
from __future__ import unicode_literals, absolute_import, print_function

import datetime

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import UpdateView, DeleteView
from gatehouseapp.filters import DataFilter
from gatehouseapp.forms import VisitCreateForm
from gatehouseapp.models import VisitData


# Create your views here.


def homePage(request):
    return render(request, 'gatehouseapp/index.html')


def pagination(strona, zmienna):
    paginator = Paginator(zmienna, 10)
    try:
        page_filter = paginator.page(strona)
    except PageNotAnInteger:
        page_filter = paginator.page(1)
    except EmptyPage:
        page_filter = paginator.page(paginator.num_pages)
    return page_filter


@login_required(login_url='/accounts/login/')
def addVisit(request):
    form = VisitCreateForm()
    visit_details = DataFilter(request.GET, queryset=VisitData.objects.filter(visit_date=datetime.date.today()).order_by('plan_hour'))
    page = request.GET.get('page')
    page_filter = pagination(page, visit_details)
    if request.method == 'POST':
        if '_add' in request.POST:
            form = VisitCreateForm(request.POST)
            if form.is_valid():
                entry = form.save(commit=False)
                entry.key_in_user = request.user
                entry.save()
                return HttpResponseRedirect(reverse('appadmin'))
        elif '_today' in request.POST:
            visit_details = DataFilter(request.GET, queryset=VisitData.objects.filter(visit_date=datetime.date.today()).order_by('plan_hour'))
            page_filter = pagination(page, visit_details)
        elif '_tomorrow' in request.POST:
            visit_details = DataFilter(request.GET, queryset=VisitData.objects.filter(visit_date__gte=datetime.date.today()+datetime.timedelta(1)).order_by('plan_hour'))
            page_filter = pagination(page, visit_details)
        elif '_arch' in request.POST:
            return HttpResponseRedirect(reverse('arch'))
    return render(request, 'gatehouseapp/addvisit.html',
        {'form': form, 'page_filter': page_filter})


class UpdateVisitData(UpdateView):
    model = VisitData
    fields = ['visit_date', 'guest', 'company', 'visit_host', 'plan_hour', 'coffe', 'lunch', 'comment' ]
    template_name = "gatehouseapp/update.html"
    success_url = reverse_lazy('appadmin')


@login_required(login_url='/accounts/login/')
def archive(request):
    form = VisitCreateForm()
    visit_details = DataFilter(request.GET, queryset=VisitData.objects.all().exclude(visit_date__gte=datetime.date.today()-datetime.timedelta(1)).order_by('plan_hour'))
    page = request.GET.get('page')
    page_filter = pagination(page, visit_details)
    if request.method == 'POST':
        if '_today' in request.POST:
            return HttpResponseRedirect(reverse('appadmin'))
    return render(request,'gatehouseapp/arch.html', {'form': form, 'page_filter': page_filter, 'filter': visit_details})


class TodayVisitForGatehouePersonListView(ListView):
    model = VisitData
    context_object_name = 'page_filter'
    template_name ='gatehouseapp/todaygatehousepersonlist.html'

    def get_queryset(self):
        return VisitData.objects.filter(visit_date=datetime.date.today())


class UpdateArriveHour(UpdateView):
    model = VisitData
    fields = ['arrive_hour',]
    template_name = "gatehouseapp/update.html"
    success_url = reverse_lazy('todayvisit')


class UpdateExitHour(UpdateView):
    model = VisitData
    fields = ['exit_hour',]
    template_name = "gatehouseapp/update.html"
    success_url = reverse_lazy('todayvisit')


class CateringListView(ListView):
    model = VisitData
    context_object_name = 'page_filter'
    template_name = 'gatehouseapp/catering.html'

    def get_queryset(self):
        return VisitData.objects.filter(Q(lunch=True, visit_date=datetime.date.today()) | Q(coffe=True, visit_date=datetime.date.today()))


class VisitDelete(DeleteView):
    model = VisitData
    template_name = "gatehouseapp/delete.html"
    success_url = reverse_lazy('appadmin')
