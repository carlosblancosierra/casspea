# Generated by Django 3.2.16 on 2023-09-26 18:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('boxes', '0021_boxsize_name'),
        ('discounts', '0004_rename_discount_type_discount_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='discount',
            name='box_exclusions',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='boxes.boxsize'),
        ),
    ]
