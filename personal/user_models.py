"""
Extensión del modelo de usuario para agregar campos personalizados.
"""
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
    Perfil extendido para usuarios del sistema.
    Agrega campos adicionales al modelo User de Django.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name="Usuario"
    )
    dni = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="DNI",
        help_text="Documento Nacional de Identidad del usuario"
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    
    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuario"
    
    def __str__(self):
        return f"{self.user.username} - DNI: {self.dni}"
