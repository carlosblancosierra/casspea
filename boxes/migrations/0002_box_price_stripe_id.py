# Generated by Django 3.2.16 on 2022-12-04 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boxes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='box',
            name='price_stripe_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
