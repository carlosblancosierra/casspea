# Generated by Django 3.2.16 on 2023-03-20 00:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boxes', '0015_alter_box_custom_chocolates_flavours'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='box',
            name='price_stripe_id',
        ),
        migrations.AddField(
            model_name='boxsize',
            name='custom_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True),
        ),
        migrations.AddField(
            model_name='boxsize',
            name='custom_price_id',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]