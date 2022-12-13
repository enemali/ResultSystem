# Generated by Django 4.0.2 on 2022-12-09 08:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0013_assessment_absentexam_assessment_absentfirstca_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=1000)),
                ('term', models.CharField(choices=[('1st-Term', '1st-Term'), ('2nd-Term', '2nd-Term'), ('3rd-Term', '3rd-Term')], max_length=100)),
                ('session', models.CharField(max_length=1000)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('className', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='result.classarmteacher')),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='result.students')),
            ],
            options={
                'ordering': ['className'],
            },
        ),
    ]