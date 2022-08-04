# Generated by Django 2.2 on 2022-07-20 16:34

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20220707_1800'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='expiry',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 20, 18, 34, 27, 968166, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='offer',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 20, 18, 34, 17, 968166, tzinfo=utc)),
        ),
    ]