# Generated by Django 3.2.16 on 2023-09-26 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boxes', '0018_auto_20230712_1520'),
    ]

    operations = [
        migrations.AddField(
            model_name='boxsize',
            name='slug',
            field=models.SlugField(blank=True),
        ),
    ]
