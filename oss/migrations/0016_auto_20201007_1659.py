# Generated by Django 3.1 on 2020-10-07 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oss', '0015_auto_20200908_2309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='installation',
            name='type',
            field=models.CharField(blank=True, choices=[('Dome', 'Dome'), ('Dish', 'Dish'), ('Enclosure', 'Enclosure'), ('Array', 'Array'), ('Gravitational Wave Detector', 'Gravitational Wave Detector'), ('Neutrino Detector', 'Neutrino Detector'), ('Spacecraft', 'Spacecraft')], default='Dome', max_length=30, null=True, verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='instrument',
            name='wavelength',
            field=models.CharField(blank=True, choices=[('Optical', 'Optical'), ('IR', 'Infrared'), ('Optical/NIR', 'Optical/Infrared'), ('UV/Optical/NIR', 'UV/Optical/Infrared'), ('Millimeter', 'Millimeter'), ('Microwave', 'Microwave'), ('Radio', 'Radio'), ('UV', 'UV'), ('Gamma ray', 'Gamma ray'), ('X-ray', 'X-ray'), ('Gravitational waves', 'Gravitational waves'), ('Neutrinos', 'Neutrinos')], default='Optical', max_length=30, null=True, verbose_name='Wavelength range/messenger'),
        ),
    ]
