# Generated by Django 4.0.2 on 2022-10-11 03:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0035_classarm_delete_namesofclasses'),
    ]

    operations = [
        migrations.RenameField(
            model_name='classarm',
            old_name='ArmName',
            new_name='armName',
        ),
    ]