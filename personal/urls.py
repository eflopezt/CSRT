"""
URLs para vistas del módulo personal.
"""
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),
    
    # Auth
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Gerencias
    path('gerencias/', views.gerencia_list, name='gerencia_list'),
    path('gerencias/crear/', views.gerencia_create, name='gerencia_create'),
    path('gerencias/<int:pk>/editar/', views.gerencia_update, name='gerencia_update'),
    
    # Áreas
    path('areas/', views.area_list, name='area_list'),
    path('areas/crear/', views.area_create, name='area_create'),
    path('areas/<int:pk>/editar/', views.area_update, name='area_update'),
    
    # Personal
    path('personal/', views.personal_list, name='personal_list'),
    path('personal/crear/', views.personal_create, name='personal_create'),
    path('personal/<int:pk>/', views.personal_detail, name='personal_detail'),
    path('personal/<int:pk>/editar/', views.personal_update, name='personal_update'),
    path('personal/exportar/', views.personal_export, name='personal_export'),
    
    # Roster
    path('roster/', views.roster_list, name='roster_list'),
    path('roster/matricial/', views.roster_matricial, name='roster_matricial'),
    path('roster/crear/', views.roster_create, name='roster_create'),
    path('roster/<int:pk>/editar/', views.roster_update, name='roster_update'),
    path('roster/exportar/', views.roster_export, name='roster_export'),
    path('roster/importar/', views.roster_import, name='roster_import'),
    path('roster/update-cell/', views.roster_update_cell, name='roster_update_cell'),
]
