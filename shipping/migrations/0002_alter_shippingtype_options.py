# Generated by Django 3.2.16 on 2023-09-23 15:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shipping', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shippingtype',
            options={'ordering': ['-default', 'cost']},
        ),
    ]
