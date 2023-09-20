# Generated by Django 4.0.2 on 2023-09-19 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0034_alter_assessment_exam_alter_assessment_firstca_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='students',
            name='current_session',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='students',
            name='current_term',
            field=models.CharField(choices=[('1', '1st-Term'), ('2', '2nd-Term'), ('3', '3rd-Term')], max_length=100, null=True),
        ),
    ]
