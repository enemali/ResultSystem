# Generated by Django 4.0.2 on 2022-12-31 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0020_remove_comment_firstcacomment_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='students',
            name='admission_number',
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='students',
            name='house',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
