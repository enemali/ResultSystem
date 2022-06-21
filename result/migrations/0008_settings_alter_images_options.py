# Generated by Django 4.0.2 on 2022-04-06 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0007_rename_image_caption_images_caption_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('announcement', models.CharField(max_length=100, null=True)),
                ('announcement_date', models.DateTimeField(auto_now_add=True)),
                ('news', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='images',
            options={'ordering': ['-id']},
        ),
    ]