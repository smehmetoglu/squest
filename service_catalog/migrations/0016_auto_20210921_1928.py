# Generated by Django 3.1.7 on 2021-09-21 17:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('service_catalog', '0015_auto_20210917_1111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestmessage',
            name='request',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', related_query_name='comment', to='service_catalog.request'),
        ),
        migrations.AlterField(
            model_name='supportmessage',
            name='support',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='supports', related_query_name='support', to='service_catalog.support'),
        ),
    ]