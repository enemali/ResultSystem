# Generated by Django 4.0.2 on 2022-11-15 12:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0009_alter_all_class_section_alter_allsubject_classname_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subjectlist',
            name='subjectSection',
        ),
    ]
