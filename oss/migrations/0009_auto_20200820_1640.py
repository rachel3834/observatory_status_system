# Generated by Django 3.1 on 2020-08-20 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oss', '0008_telescope_tel_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telescope',
            name='tel_code',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Telescope code'),
        ),
    ]
