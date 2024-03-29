# Generated by Django 3.2.16 on 2024-01-22 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flavours', '0005_flavour_mini_description'),
        ('boxes', '0024_boxsize_weight'),
    ]

    operations = [
        migrations.AddField(
            model_name='boxsize',
            name='prebuild_options',
            field=models.ManyToManyField(blank=True, related_name='prebuild_options', to='flavours.PreBuildFlavour'),
        ),
    ]
