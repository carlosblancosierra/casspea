# Generated by Django 3.2.16 on 2023-09-23 15:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shipping', '0002_alter_shippingtype_options'),
        ('carts', '0005_cart_shipping_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='subtotal',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='total',
        ),
        migrations.AlterField(
            model_name='cart',
            name='shipping_type',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shipping.shippingtype'),
        ),
    ]
