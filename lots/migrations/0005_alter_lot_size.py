# Generated by Django 3.2.16 on 2023-04-17 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lots', '0004_remove_lot_pre_built'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lot',
            name='size',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
