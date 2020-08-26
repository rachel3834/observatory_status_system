# Generated by Django 3.1 on 2020-08-25 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oss', '0009_auto_20200820_1640'),
    ]

    operations = [
        migrations.AddField(
            model_name='facilityoperator',
            name='url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='instrument',
            name='url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='site',
            name='url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='telescope',
            name='url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
