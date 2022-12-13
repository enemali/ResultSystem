# Generated by Django 4.0.2 on 2022-12-09 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0014_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='Aesthetic_Appreciation',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AddField(
            model_name='comment',
            name='Attendance_in_Class',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AddField(
            model_name='comment',
            name='Crafts',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AddField(
            model_name='comment',
            name='Creativity',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AddField(
            model_name='comment',
            name='Fluency',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AddField(
            model_name='comment',
            name='Games',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AddField(
            model_name='comment',
            name='Handling_of_Tools',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AddField(
            model_name='comment',
            name='Handwriting',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AddField(
            model_name='comment',
            name='Honesty',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AddField(
            model_name='comment',
            name='Leadership_Role',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AddField(
            model_name='comment',
            name='Musical_Skills',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AddField(
            model_name='comment',
            name='Neatness',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AddField(
            model_name='comment',
            name='Number_of_Times_Present',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AddField(
            model_name='comment',
            name='Obedience',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AddField(
            model_name='comment',
            name='Painting_and_Drawing',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AddField(
            model_name='comment',
            name='Politeness',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AddField(
            model_name='comment',
            name='Punctuality',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AddField(
            model_name='comment',
            name='Self_Control',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AddField(
            model_name='comment',
            name='Sense_of_Responsibility',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AddField(
            model_name='comment',
            name='Sociability',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AddField(
            model_name='comment',
            name='Sports',
            field=models.CharField(blank=True, max_length=1000),
        ),
    ]
