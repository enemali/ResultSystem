# Generated by Django 4.0.2 on 2024-03-02 17:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0038_remove_setting_unique_is_current_setting_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='setting',
            name='announcement',
        ),
        migrations.RemoveField(
            model_name='setting',
            name='announcement_date',
        ),
        migrations.RemoveField(
            model_name='setting',
            name='current_Session',
        ),
        migrations.RemoveField(
            model_name='setting',
            name='current_Term',
        ),
        migrations.RemoveField(
            model_name='setting',
            name='date_Term_Begin',
        ),
        migrations.RemoveField(
            model_name='setting',
            name='date_Term_End',
        ),
        migrations.RemoveField(
            model_name='setting',
            name='news',
        ),
        migrations.RemoveField(
            model_name='setting',
            name='next_term_begins',
        ),
        migrations.RemoveField(
            model_name='setting',
            name='number_of_days_school_open',
        ),
    ]
