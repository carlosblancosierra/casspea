# Generated by Django 3.2.16 on 2023-04-12 13:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('custom_chocolates', '0010_alter_userchocolatedesign_options'),
        ('lots', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lot',
            name='custom_design',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='custom_chocolates.userchocolatedesign'),
        ),
    ]
