# Generated by Django 4.0.2 on 2022-10-14 10:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0043_alter_students_classarm'),
    ]

    operations = [
        migrations.AlterField(
            model_name='students',
            name='classArm',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='studentclassArm', to='result.classarm'),
        ),
    ]