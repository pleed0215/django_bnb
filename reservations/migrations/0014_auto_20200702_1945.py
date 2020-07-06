# Generated by Django 2.2.5 on 2020-07-02 10:45

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0013_auto_20200702_1928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='checkin_date',
            field=models.DateField(default=datetime.datetime(2020, 7, 2, 10, 45, 0, 257420, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='checkout_date',
            field=models.DateField(default=datetime.datetime(2020, 7, 2, 10, 45, 0, 257456, tzinfo=utc), null=True),
        ),
    ]