# Generated by Django 3.1 on 2020-10-16 23:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oss', '0018_auto_20201016_2350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='installation',
            name='type',
            field=models.CharField(blank=True, choices=[('Dome', 'Dome'), ('Dish', 'Dish'), ('Enclosure', 'Enclosure'), ('Array', 'Array'), ('Gravitational Wave Detector', 'Gravitational Wave Detector'), ('Neutrino Detector', 'Neutrino Detector'), ('Detector', 'Detector'), ('Spacecraft', 'Spacecraft')], default='Dome', max_length=30, null=True, verbose_name='Type'),
        ),
    ]