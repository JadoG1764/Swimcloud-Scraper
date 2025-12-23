from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page),
    path('races/', views.races_page),
    path('swimmers/', views.swimmers_page),
    path('teams/', views.teams_page),
]