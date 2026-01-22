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
    path('logout/', views.logout_view, name='logout'),
    
    # Áreas
    path('areas/', views.area_list, name='area_list'),
    path('areas/crear/', views.area_create, name='area_create'),
    path('areas/<int:pk>/editar/', views.area_update, name='area_update'),
    path('areas/exportar/', views.area_export, name='area_export'),
    path('areas/importar/', views.area_import, name='area_import'),
    
    # SubÁreas
    path('subareas/', views.subarea_list, name='subarea_list'),
    path('subareas/crear/', views.subarea_create, name='subarea_create'),
    path('subareas/<int:pk>/editar/', views.subarea_update, name='subarea_update'),
    path('subareas/exportar/', views.subarea_export, name='subarea_export'),
    path('subareas/importar/', views.subarea_import, name='subarea_import'),
    
    # Personal
    path('personal/', views.personal_list, name='personal_list'),
    path('personal/crear/', views.personal_create, name='personal_create'),
    path('personal/<int:pk>/', views.personal_detail, name='personal_detail'),
    path('personal/<int:pk>/editar/', views.personal_update, name='personal_update'),
    path('personal/exportar/', views.personal_export, name='personal_export'),
    path('personal/importar/', views.personal_import, name='personal_import'),
    
    # Roster
    # path('roster/', views.roster_list, name='roster_list'),  # Oculto
    path('roster/matricial/', views.roster_matricial, name='roster_matricial'),
    path('roster/crear/', views.roster_create, name='roster_create'),
    path('roster/<int:pk>/editar/', views.roster_update, name='roster_update'),
    path('roster/exportar/', views.roster_export, name='roster_export'),
    path('roster/importar/', views.roster_import, name='roster_import'),
    path('roster/update-cell/', views.roster_update_cell, name='roster_update_cell'),
    
    # Sistema de Aprobaciones
    path('aprobaciones/', views.dashboard_aprobaciones, name='dashboard_aprobaciones'),
    path('roster/cambios-pendientes/', views.cambios_pendientes, name='cambios_pendientes'),
    path('roster/aprobar/<int:pk>/', views.aprobar_cambio, name='aprobar_cambio'),
    path('roster/rechazar/<int:pk>/', views.rechazar_cambio, name='rechazar_cambio'),
    path('roster/enviar-aprobacion/', views.enviar_cambios_aprobacion, name='enviar_cambios_aprobacion'),
    path('roster/aprobar-lote/', views.aprobar_lote, name='aprobar_lote'),
    path('roster/rechazar-lote/', views.rechazar_lote, name='rechazar_lote'),
    
    # Gestión de Usuarios
    path('usuarios/', views.usuario_list, name='usuario_list'),
    path('usuarios/vincular/', views.usuario_vincular, name='usuario_vincular'),
    path('usuarios/crear-vincular/', views.usuario_crear_y_vincular, name='usuario_crear_y_vincular'),
    path('usuarios/desvincular/<int:user_id>/', views.usuario_desvincular, name='usuario_desvincular'),
]
