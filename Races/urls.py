from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page),
    path('CCCAA/', views.CCCAA_page),
    path('CCS/', views.CCS_page),
    path('CCCAA/races/', views.CCCAA_races_page),
    path('CCS/races/', views.CCS_races_page),
    path('CCCAA/swimmers/', views.swimmers_page),
    path('CCCAA/teams/', views.teams_page),
    path('swimmers/<str:name>/', views.swimmers_slug),
    path('swimmers_redirect/', views.swimmer_redirect, name='swimmers_redirect'),
    path('teams/<str:name>/', views.teams_slug),
]