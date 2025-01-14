from django.shortcuts import render
from pages.models import Page, Statistics


def index(request):
    page = Page.objects.first()
    return render(request, 'pages/index.html', {'page': page})


def statistics(request):
    statistic = Statistics.objects.prefetch_related('tables').all()
    return render(request, 'pages/statistics.html', {'statistic': statistic})


def demand(request):
    return render(request, 'pages/demand.html')


def geography(request):
    return render(request, 'pages/geography.html')


def skills(request):
    return render(request, 'pages/skills.html')


def vacancies(request):
    return render(request, 'pages/vacancies.html')