# Generated by Django 4.0.2 on 2022-10-11 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0037_alter_students_classarm'),
    ]

    operations = [
        migrations.AlterField(
            model_name='students',
            name='classArm',
            field=models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'), ('F', 'F'), ('G', 'G'), ('H', 'H'), ('I', 'I'), ('J', 'J'), ('K', 'K'), ('L', 'L'), ('M', 'M'), ('N', 'N'), ('O', 'O'), ('P', 'P'), ('Q', 'Q'), ('R', 'R'), ('S', 'S'), ('T', 'T'), ('U', 'U'), ('V', 'V'), ('W', 'W'), ('X', 'X'), ('Y', 'Y'), ('Z', 'Z')], default='A', max_length=100),
            preserve_default=False,
        ),
    ]