# Generated by Django 3.2.7 on 2024-02-09 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0034_domain_ahrefs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='domain',
            name='status',
            field=models.IntegerField(choices=[(0, 'added'), (1, 'check files'), (2, 'inprogress'), (3, 'get images'), (4, 'checked'), (5, 'get files'), (6, 'timestamps'), (7, 'ahrefs')], default=0),
        ),
    ]
