from django.urls import path
from . import views
from . import pdf

urlpatterns = [
    path('', views.home_page),
    path('<str:division>/', views.division_page),
    path('<str:division>/races/', views.races_page),
    path('<str:division>/races/downloadpdf/', pdf.pdf_download),
    path('<str:division>/swimmers/', views.swimmers_page),
    path('<str:division>/teams/', views.teams_page),
    path('swimmers/<str:name>/', views.swimmers_slug),
    path('swimmers_redirect/', views.swimmer_redirect, name='swimmers_redirect'),
    path('teams/<str:name>/', views.teams_slug),
]