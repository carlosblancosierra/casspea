# Generated by Django 3.2.16 on 2023-03-17 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flavours', '0004_auto_20221219_0947'),
        ('boxes', '0014_auto_20230317_1404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='box',
            name='custom_chocolates_flavours',
            field=models.ManyToManyField(blank=True, to='flavours.Flavour'),
        ),
    ]