# Generated by Django 4.0.2 on 2023-01-01 13:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0022_alter_students_admission_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='Aesthetic_Appreciation',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='Crafts',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='Games',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='Handling_of_Tools',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='Handwriting',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='Musical_Skills',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='Painting_and_Drawing',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='Politeness',
        ),
    ]
