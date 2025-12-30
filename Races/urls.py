from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page),
    path('races/', views.races_page),
    path('swimmers/', views.swimmers_page),
    path('teams/', views.teams_page),
    path('swimmers/<str:name>/', views.swimmers_slug),
    path('swimmers_redirect/', views.swimmer_redirect, name='swimmers_redirect'),
    path('teams/<str:name>/', views.teams_slug),
]