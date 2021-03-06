# Generated by Django 2.2 on 2022-06-28 14:58

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='expiry',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 28, 16, 58, 41, 943052, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='article',
            name='user',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='app.Profile'),
        ),
        migrations.AlterField(
            model_name='offer',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 28, 16, 58, 11, 943052, tzinfo=utc)),
        ),
    ]
