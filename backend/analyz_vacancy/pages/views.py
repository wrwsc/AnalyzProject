from itertools import chain

from django.shortcuts import render
from pages.models import Page, Statistics, StatisticsTable, DemandStatisticsTable, DemandStatistics, GeoStatistics,\
    GeoStatisticsTable, SkillStatistics, SkillStatisticsTable


def index(request):
    page = Page.objects.first()
    return render(request, 'pages/index.html', {'page': page})


def statistics(request):
    statistics = Statistics.objects.all()
    tables = StatisticsTable.objects.all()
    return render(request, 'pages/statistics.html', {'statistics': statistics, 'tables': tables})


def demand(request):
    demand_statistics = DemandStatistics.objects.all()
    demand_tables = DemandStatisticsTable.objects.all()
    return render(request, 'pages/demand.html', {'demand_statistics': demand_statistics, 'demand_tables': demand_tables})


def geography(request):
    geo_statistics = GeoStatistics.objects.all()
    geo_tables = GeoStatisticsTable.objects.all()
    return render(request, 'pages/geography.html', {'geo_statistics': geo_statistics, 'geo_tables': geo_tables})


def skills(request):
    skill_statistics = SkillStatistics.objects.all()
    skill_tables = SkillStatisticsTable.objects.all()
    return render(request, 'pages/skills.html', {'skill_statistics': skill_statistics, 'skill_tables': skill_tables})


def vacancies(request):
    return render(request, 'pages/vacancies.html')