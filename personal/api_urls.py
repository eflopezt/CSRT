"""
URLs para la API REST del módulo personal.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import (
    AreaViewSet, SubAreaViewSet, PersonalViewSet,
    RosterViewSet, RosterAuditViewSet
)

router = DefaultRouter()
router.register(r'gerencias', AreaViewSet, basename='area')
router.register(r'subareas', SubAreaViewSet, basename='subarea')
router.register(r'personal', PersonalViewSet, basename='personal')
router.register(r'roster', RosterViewSet, basename='roster')
router.register(r'roster-audit', RosterAuditViewSet, basename='roster-audit')

urlpatterns = [
    path('', include(router.urls)),
]
