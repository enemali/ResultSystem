# Generated by Django 4.0.2 on 2022-11-18 05:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0011_subjectlist_subjectsection'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='allsubject',
            options={'ordering': ['className']},
        ),
    ]
