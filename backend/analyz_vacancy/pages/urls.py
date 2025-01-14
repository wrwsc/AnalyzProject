from django.conf.urls.static import static
from django.urls import path

from analyz_vacancy import settings
from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.index, name='index'),
    path('statistics/', views.statistics, name='statistics'),
    path('demand/', views.demand, name = 'demand'),
    path('geography/', views.geography, name = 'geography'),
    path('skills/', views.skills, name = 'skills'),
    path('vacancies/', views.vacancies, name = 'vacancies'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
