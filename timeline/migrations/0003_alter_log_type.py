# Generated by Django 4.0.6 on 2022-08-23 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timeline', '0002_alter_log_type_alter_request_requesttype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='type',
            field=models.CharField(choices=[('SENT', 'SENT'), ('RECEIVED', 'RECEIVED')], max_length=8),
        ),
    ]
