# Generated by Django 4.0.2 on 2022-10-09 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0030_remove_users_groups_remove_users_user_permissions_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='students',
            name='user',
        ),
        migrations.AddField(
            model_name='students',
            name='gender',
            field=models.CharField(choices=[('Male', 'male'), ('Female', 'female')], default='male', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='students',
            name='middle_name',
            field=models.CharField(default='kate', max_length=100),
            preserve_default=False,
        ),
    ]