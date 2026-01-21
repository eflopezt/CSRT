"""
Signals para el módulo personal.
"""
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Roster, RosterAudit


@receiver(pre_save, sender=Roster)
def audit_roster_changes(sender, instance, **kwargs):
    """
    Registra cambios en el roster antes de guardar.
    """
    if instance.pk:  # Solo si ya existe (actualización)
        try:
            old_instance = Roster.objects.get(pk=instance.pk)
            
            # Verificar cambios en campos relevantes
            campos_a_auditar = ['codigo', 'observaciones']
            
            for campo in campos_a_auditar:
                valor_anterior = str(getattr(old_instance, campo))
                valor_nuevo = str(getattr(instance, campo))
                
                if valor_anterior != valor_nuevo:
                    # Crear registro de auditoría
                    RosterAudit.objects.create(
                        personal=instance.personal,
                        fecha=instance.fecha,
                        campo_modificado=campo,
                        valor_anterior=valor_anterior,
                        valor_nuevo=valor_nuevo,
                        usuario=None  # Se puede obtener del request en la vista
                    )
        except Roster.DoesNotExist:
            pass
