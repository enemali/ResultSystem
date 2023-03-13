# Generated by Django 4.0.2 on 2023-02-05 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0029_rename_settingtype_setting_setting_type_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='setting',
            old_name='current_setting',
            new_name='is_current_setting',
        ),
        migrations.AddConstraint(
            model_name='setting',
            constraint=models.UniqueConstraint(condition=models.Q(('is_current_setting', True)), fields=('is_current_setting',), name='unique_is_current_setting'),
        ),
    ]