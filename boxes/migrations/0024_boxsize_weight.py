# Generated by Django 3.2.16 on 2024-01-19 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boxes', '0023_boxsize_valentines_box'),
    ]

    operations = [
        migrations.AddField(
            model_name='boxsize',
            name='weight',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
