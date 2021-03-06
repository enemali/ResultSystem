# Generated by Django 4.0.2 on 2022-04-01 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0005_alter_all_class_classname_alter_section_sectionname'),
    ]

    operations = [
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('image_caption', models.CharField(max_length=100, null=True)),
                ('image_description', models.CharField(max_length=100, null=True)),
            ],
        ),
    ]
