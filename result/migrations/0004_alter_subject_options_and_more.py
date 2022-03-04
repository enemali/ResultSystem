# Generated by Django 4.0.2 on 2022-03-04 01:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0003_subject_students_assessment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subject',
            options={'ordering': ['subjectName']},
        ),
        migrations.RenameField(
            model_name='subject',
            old_name='subject',
            new_name='subjectName',
        ),
        migrations.AlterField(
            model_name='subject',
            name='classNmame',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subjectclass', to='result.all_class'),
        ),
    ]
