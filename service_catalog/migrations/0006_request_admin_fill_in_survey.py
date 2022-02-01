# Generated by Django 3.2.11 on 2022-02-02 10:00

from django.db import migrations, models

from service_catalog.models import Request


def split_fill_in_survey(apps, schema_editor):
    for request in Request.objects.all():
        request.set_fill_in_survey(request.fill_in_survey)


class Migration(migrations.Migration):

    dependencies = [
        ('service_catalog', '0005_auto_20220201_1557'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='admin_fill_in_survey',
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.RunPython(split_fill_in_survey),
    ]