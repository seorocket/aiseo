# Generated by Django 3.2.7 on 2023-10-17 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_alter_file_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='url',
            field=models.CharField(max_length=1255000, unique=True),
        ),
    ]