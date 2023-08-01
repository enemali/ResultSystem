# Generated by Django 4.0.2 on 2023-08-01 09:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0031_alter_assessment_exam_alter_assessment_firstca_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assessment',
            name='exam',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='assessment',
            name='firstCa',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(20), django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='assessment',
            name='secondCa',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(20), django.core.validators.MinValueValidator(0)]),
        ),
    ]