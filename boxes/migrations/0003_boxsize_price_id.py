# Generated by Django 3.2.16 on 2022-12-05 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boxes', '0002_box_price_stripe_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='boxsize',
            name='price_id',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
