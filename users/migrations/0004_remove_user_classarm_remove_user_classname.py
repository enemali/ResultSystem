# Generated by Django 4.0.2 on 2022-11-03 22:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_classarm_user_classname'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='classArm',
        ),
        migrations.RemoveField(
            model_name='user',
            name='className',
        ),
    ]