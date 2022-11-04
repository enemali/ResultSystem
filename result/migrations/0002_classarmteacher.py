# Generated by Django 4.0.2 on 2022-11-03 15:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('result', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='classArmTeacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('classArm', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='result.classarm')),
                ('className', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='result.all_class')),
                ('classTeacher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['className'],
            },
        ),
    ]
