# Generated by Django 4.2.13 on 2024-12-09 14:01
from django.db import migrations, models
import django.db.models.deletion

import service_catalog.models.operations


def set_perm_to_operations(apps, schema_editor):
    """
    In order to delete the "is_admin_operation" flag we need to set new permission
    By default: view_operation
    If was admin operation: is_admin_operation
    """
    Permission = apps.get_model('profiles', 'Permission')
    Operation = apps.get_model('service_catalog', 'Operation')
    ContentType = apps.get_model('contenttypes', 'ContentType')
    operation_content_type = ContentType.objects.get_for_model(Operation)

    view_admin_operation, _ = Permission.objects.get_or_create(codename="view_admin_operation", content_type=operation_content_type)
    view_operation, _ = Permission.objects.get_or_create(codename="view_operation", content_type=operation_content_type)
    Operation.objects.filter(is_admin_operation=True).update(permission=view_admin_operation)
    Operation.objects.filter(is_admin_operation=False).update(permission=view_operation)


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0023_notificationstatefield'),
        ('service_catalog', '0043_operation_when'),
    ]

    operations = [
        migrations.AddField(
            model_name='operation',
            name='permission',
            field=models.ForeignKey(blank=True, limit_choices_to={'content_type__app_label': 'service_catalog', 'content_type__model': 'operation'}, help_text='Permission to view the operation. Evaluated only at Global Scope and Default Permission level',null=True, on_delete=django.db.models.deletion.PROTECT, related_name='operation', to='profiles.permission'),
        ),
        migrations.RunPython(set_perm_to_operations),
        migrations.AlterField(
            model_name='operation',
            name='permission',
            field=models.ForeignKey(
                limit_choices_to={'content_type__app_label': 'service_catalog', 'content_type__model': 'operation'},
                on_delete=django.db.models.deletion.PROTECT, related_name='operation', to='profiles.permission',
                help_text='Permission to view the operation. Evaluated only at Global Scope and Default Permission level',
                default=service_catalog.models.operations.get_default_permission_pk
            )

        ),
        migrations.RemoveField(
            model_name='operation',
            name='is_admin_operation',
        ),
        migrations.AlterModelOptions(
            name='instance',
            options={'default_permissions': ('add', 'change', 'delete', 'view', 'list'), 'ordering': ['-last_updated'],
                     'permissions': [('archive_instance', 'Can archive instance'),
                                     ('unarchive_instance', 'Can unarchive instance'),
                                     ("request_on_instance", "Can request a day2 operation on instance"),
                                     ('view_admin_spec_instance', 'Can view admin spec on instance'),
                                     ('change_admin_spec_instance', 'Can change admin spec on instance'),
                                     ('rename_instance', 'Can rename instance'),
                                     ('change_requester_on_instance', 'Can change owner of the instance')]},
        ),
    ]