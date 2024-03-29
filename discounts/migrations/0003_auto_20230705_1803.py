# Generated by Django 3.2.16 on 2023-07-05 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discounts', '0002_auto_20230705_1739'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='discount',
            name='is_percentage',
        ),
        migrations.AddField(
            model_name='discount',
            name='discount_type',
            field=models.CharField(choices=[('Percentage', 'Percentage'), ('Fixed Amount', 'Fixed Amount')], default='Percentage', max_length=20),
        ),
        migrations.AlterField(
            model_name='discount',
            name='code',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='discount',
            name='stripe_id',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='discount',
            name='title',
            field=models.CharField(max_length=255),
        ),
    ]
