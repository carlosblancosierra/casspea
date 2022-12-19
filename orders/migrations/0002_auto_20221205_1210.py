# Generated by Django 3.2.16 on 2022-12-05 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(blank=True, choices=[('created', 'created'), ('cancelled', 'cancelled'), ('paid', 'paid'), ('delivered', 'delivered')], default='created', max_length=120),
        ),
    ]