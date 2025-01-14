from itertools import chain

from django.shortcuts import render
from pages.models import Page, Statistics, StatisticsTable


def index(request):
    page = Page.objects.first()
    return render(request, 'pages/index.html', {'page': page})


def statistics(request):
    statistics = Statistics.objects.all()
    tables = StatisticsTable.objects.all()
    return render(request, 'pages/statistics.html', {'statistics': statistics, 'tables': tables})


def demand(request):
    return render(request, 'pages/demand.html')


def geography(request):
    return render(request, 'pages/geography.html')


def skills(request):
    return render(request, 'pages/skills.html')


def vacancies(request):
    return render(request, 'pages/vacancies.html')