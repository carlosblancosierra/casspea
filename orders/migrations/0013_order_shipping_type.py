# Generated by Django 3.2.16 on 2023-09-23 15:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shipping', '0002_alter_shippingtype_options'),
        ('orders', '0012_order_staff_email_sent'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='shipping_type',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shipping.shippingtype'),
        ),
    ]
