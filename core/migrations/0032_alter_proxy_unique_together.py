# Generated by Django 3.2.7 on 2023-10-26 08:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0031_auto_20231025_2029'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='proxy',
            unique_together={('ip_address', 'port')},
        ),
    ]
