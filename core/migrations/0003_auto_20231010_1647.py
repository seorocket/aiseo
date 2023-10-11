# Generated by Django 3.2.7 on 2023-10-10 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20230829_1256'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='searchquery',
            name='clicks',
        ),
        migrations.RemoveField(
            model_name='searchquery',
            name='ctr',
        ),
        migrations.RemoveField(
            model_name='searchquery',
            name='demand',
        ),
        migrations.RemoveField(
            model_name='searchquery',
            name='impressions',
        ),
        migrations.RemoveField(
            model_name='searchquery',
            name='position',
        ),
        migrations.AddField(
            model_name='searchquery',
            name='status',
            field=models.IntegerField(choices=[(0, 'added'), (1, 'done'), (2, 'inprogress')], default=0),
        ),
        migrations.AlterField(
            model_name='domain',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]