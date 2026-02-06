from django.db import migrations, models


def forwards_copy_responsables(apps, schema_editor):
    Area = apps.get_model("personal", "Area")
    for area in Area.objects.exclude(responsable__isnull=True):
        if area.responsable_id:
            area.responsables.add(area.responsable_id)


def backwards_copy_responsable(apps, schema_editor):
    Area = apps.get_model("personal", "Area")
    for area in Area.objects.all():
        primero = area.responsables.first()
        area.responsable = primero
        area.save(update_fields=["responsable"])


class Migration(migrations.Migration):
    dependencies = [
        ("personal", "0008_rename_models_area_subarea"),
    ]

    operations = [
        migrations.AddField(
            model_name="area",
            name="responsables",
            field=models.ManyToManyField(
                blank=True,
                help_text="Personas responsables de esta area",
                related_name="areas_responsable",
                to="personal.personal",
                verbose_name="Responsables",
            ),
        ),
        migrations.RunPython(forwards_copy_responsables, backwards_copy_responsable),
        migrations.RemoveField(
            model_name="area",
            name="responsable",
        ),
    ]
