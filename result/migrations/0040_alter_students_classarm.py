# Generated by Django 4.0.2 on 2022-10-11 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0039_alter_classarm_options_remove_classarm_classname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='students',
            name='classArm',
            field=models.CharField(max_length=100),
        ),
    ]
