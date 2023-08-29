# Generated by Django 3.2.7 on 2023-08-29 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='searchquery',
            name='clicks',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='searchquery',
            name='ctr',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='searchquery',
            name='demand',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='searchquery',
            name='impressions',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='searchquery',
            name='position',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
    ]
