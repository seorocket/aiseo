# Generated by Django 3.2.7 on 2023-10-23 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_searchquery_status_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='shot',
            name='digest',
            field=models.CharField(default=1, max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shot',
            name='length',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shot',
            name='statuscode',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shot',
            name='timestamp',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='shot',
            name='name',
            field=models.CharField(max_length=99999, verbose_name='Shot'),
        ),
    ]
