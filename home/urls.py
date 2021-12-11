from django.urls import path

from . import views

app_name = 'home'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('informations/', views.InformationsView.as_view(), name='informations'),
    path('devInformations/', views.DevInformationsView.as_view(), name='devInformations'),
]