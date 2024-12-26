from django.shortcuts import render


def index(request):
    return render(request, 'pages/index.html')


def statistics(request):
    return render(request, 'pages/statistics.html')


def demand(request):
    return render(request, 'pages/demand.html')


def geography(request):
    return render(request, 'pages/geography.html')


def skills(request):
    return render(request, 'pages/skills.html')


def vacancies(request):
    return render(request, 'pages/vacancies.html')