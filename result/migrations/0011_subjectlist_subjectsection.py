# Generated by Django 4.0.2 on 2022-11-16 21:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0010_remove_subjectlist_subjectsection'),
    ]

    operations = [
        migrations.AddField(
            model_name='subjectlist',
            name='subjectSection',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='result.section'),
        ),
    ]
