# Generated by Django 4.0.6 on 2022-09-16 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timeline', '0003_alter_log_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='data',
            name='hostname',
        ),
        migrations.RemoveField(
            model_name='data',
            name='result',
        ),
        migrations.RemoveField(
            model_name='data',
            name='role',
        ),
        migrations.AddField(
            model_name='data',
            name='data',
            field=models.CharField(default=None, max_length=4096),
            preserve_default=False,
        ),
    ]
