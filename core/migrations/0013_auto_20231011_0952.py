# Generated by Django 3.2.7 on 2023-10-11 06:52

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_textpage'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='textpage',
            options={'verbose_name': 'page', 'verbose_name_plural': 'Pages'},
        ),
        migrations.AlterField(
            model_name='textpage',
            name='content',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='textpage',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]
