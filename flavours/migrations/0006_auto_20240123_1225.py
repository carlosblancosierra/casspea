# Generated by Django 3.2.16 on 2024-01-23 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flavours', '0005_flavour_mini_description'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='prebuildflavour',
            options={'ordering': ['-updated']},
        ),
        migrations.AddField(
            model_name='flavour',
            name='valentines_flavour',
            field=models.BooleanField(default=False),
        ),
    ]
