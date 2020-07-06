# Generated by Django 2.2.5 on 2020-07-01 14:55

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0007_auto_20200701_2331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='checkin_date',
            field=models.DateField(default=datetime.datetime(2020, 7, 1, 14, 55, 14, 811580, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='checkout_date',
            field=models.DateField(default=datetime.datetime(2020, 7, 1, 14, 55, 14, 811580, tzinfo=utc), null=True),
        ),
    ]