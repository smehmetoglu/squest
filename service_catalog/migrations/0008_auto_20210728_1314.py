# Generated by Django 3.1.7 on 2021-07-28 13:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('service_catalog', '0007_globalhook_servicestatehook'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operation',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='operations', related_query_name='operation', to='service_catalog.service'),
        ),
    ]