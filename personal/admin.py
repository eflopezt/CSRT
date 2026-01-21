"""
Configuración del admin para el módulo personal.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Gerencia, Area, Personal, Roster, RosterAudit
from .user_models import UserProfile


# Inline para mostrar el perfil dentro del admin de User
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Perfil con DNI'
    fk_name = 'user'


# Extender el UserAdmin para incluir el perfil
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ['username', 'email', 'first_name', 'last_name', 'get_dni', 'is_staff']
    
    def get_dni(self, obj):
        try:
            return obj.profile.dni
        except UserProfile.DoesNotExist:
            return '-'
    get_dni.short_description = 'DNI'


# Re-registrar UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Gerencia)
class GerenciaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'responsable', 'activa', 'creado_en']
    list_filter = ['activa', 'creado_en']
    search_fields = ['nombre', 'responsable__apellidos_nombres']
    raw_id_fields = ['responsable']


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'gerencia', 'activa', 'creado_en']
    list_filter = ['gerencia', 'activa', 'creado_en']
    search_fields = ['nombre', 'gerencia__nombre']


@admin.register(Personal)
class PersonalAdmin(admin.ModelAdmin):
    list_display = [
        'apellidos_nombres', 'nro_doc', 'cargo', 'area',
        'estado', 'fecha_alta', 'tipo_trab', 'dias_libres_corte_2025'
    ]
    list_filter = ['estado', 'tipo_trab', 'area__gerencia', 'area']
    search_fields = ['apellidos_nombres', 'nro_doc', 'cargo', 'celular']
    raw_id_fields = ['usuario', 'area']
    fieldsets = (
        ('Información Básica', {
            'fields': ('usuario', 'tipo_doc', 'nro_doc', 'apellidos_nombres', 'codigo_fotocheck')
        }),
        ('Datos Laborales', {
            'fields': ('cargo', 'tipo_trab', 'area', 'fecha_alta', 'fecha_cese', 'estado',
                      'regimen_laboral', 'regimen_turno')
        }),
        ('Roster', {
            'fields': ('dias_libres_corte_2025',)
        }),
        ('Datos Personales', {
            'fields': ('fecha_nacimiento', 'sexo', 'celular', 'correo_personal',
                      'correo_corporativo', 'direccion', 'ubigeo')
        }),
        ('Datos Financieros', {
            'fields': ('sueldo_base', 'bonos', 'afp', 'banco',
                      'cuenta_ahorros', 'cuenta_cci', 'cuenta_cts')
        }),
        ('Observaciones', {
            'fields': ('observaciones',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Roster)
class RosterAdmin(admin.ModelAdmin):
    list_display = ['personal', 'fecha', 'codigo', 'observaciones']
    list_filter = ['fecha', 'personal__area']
    search_fields = ['personal__apellidos_nombres', 'personal__nro_doc', 'codigo']
    raw_id_fields = ['personal']
    date_hierarchy = 'fecha'


@admin.register(RosterAudit)
class RosterAuditAdmin(admin.ModelAdmin):
    list_display = ['personal', 'fecha', 'campo_modificado', 'usuario', 'creado_en']
    list_filter = ['campo_modificado', 'creado_en']
    search_fields = ['personal__apellidos_nombres', 'personal__nro_doc']
    raw_id_fields = ['personal', 'usuario']
    date_hierarchy = 'creado_en'
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
