# Generated by Django 5.1.6 on 2025-02-10 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_posts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='postsmodel',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
