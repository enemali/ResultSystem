# Generated by Django 4.0.2 on 2022-06-07 02:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0014_alter_subject_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setting',
            name='announcement_date',
            field=models.DateField(null=True),
        ),
    ]