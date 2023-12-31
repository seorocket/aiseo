# Generated by Django 3.2.7 on 2023-10-10 19:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_file_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=99999, verbose_name='ID')),
                ('date', models.DateField(default='1000-01-01')),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.file')),
            ],
            options={
                'verbose_name': 'Snapshot',
                'verbose_name_plural': "Snapshot's",
            },
        ),
    ]
