# Generated by Django 3.2.16 on 2022-12-05 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20221205_1210'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='stripe_data',
            field=models.TextField(blank=True, null=True),
        ),
    ]
