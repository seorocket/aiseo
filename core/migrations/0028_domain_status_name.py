# Generated by Django 3.2.7 on 2023-10-23 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_alter_domain_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='domain',
            name='status_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
