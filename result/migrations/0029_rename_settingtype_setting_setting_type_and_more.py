# Generated by Django 4.0.2 on 2023-02-05 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0028_assessment_recordedby_setting_settingtype_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='setting',
            old_name='settingType',
            new_name='setting_type',
        ),
        migrations.RenameField(
            model_name='setting',
            old_name='settingValue',
            new_name='setting_value',
        ),
        migrations.AddField(
            model_name='setting',
            name='current_setting',
            field=models.BooleanField(default=False),
        ),
    ]
