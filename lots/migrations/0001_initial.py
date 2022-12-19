# Generated by Django 3.2.16 on 2022-12-19 12:21

from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields
import lots.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('flavours', '0004_auto_20221219_0947'),
    ]

    operations = [
        migrations.CreateModel(
            name='LotSize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.PositiveIntegerField()),
                ('description', models.TextField(blank=True, null=True)),
                ('price_id', models.CharField(blank=True, max_length=200, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('active', models.BooleanField(default=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('image', imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to=lots.models.upload_location)),
                ('image2', imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to=lots.models.upload_location)),
                ('image3', imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to=lots.models.upload_location)),
                ('image4', imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to=lots.models.upload_location)),
                ('image5', imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to=lots.models.upload_location)),
            ],
        ),
        migrations.CreateModel(
            name='Lot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flavour_format', models.CharField(choices=[('custom', 'Custom'), ('pre_built', 'Pre-Built'), ('pick_and_mix', 'Pick and Mix')], default='pre_built', max_length=30)),
                ('price_stripe_id', models.CharField(blank=True, max_length=100, null=True)),
                ('active', models.BooleanField(default=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('pre_built', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='flavours.prebuildflavour')),
                ('selected_flavours', models.ManyToManyField(blank=True, related_name='lot_selected_flavours', to='flavours.FlavourChoice')),
                ('selected_prebuilts', models.ManyToManyField(blank=True, related_name='lot_selected_prebuilts', to='flavours.PreBuildFlavour')),
                ('size', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='lots.lotsize')),
            ],
        ),
    ]