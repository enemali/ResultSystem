# Generated by Django 4.0.2 on 2024-03-21 04:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0040_alter_comment_number_of_days_school_open_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='term',
            field=models.CharField(max_length=100),
        ),
    ]
