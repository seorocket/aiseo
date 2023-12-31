# Generated by Django 3.2.7 on 2023-10-17 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_auto_20231017_2159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='endtimestamp',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='file',
            name='groupcount',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='file',
            name='mimetype',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='file',
            name='timestamp',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='file',
            name='uniqcount',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
