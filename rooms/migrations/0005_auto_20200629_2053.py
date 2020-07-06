# Generated by Django 2.2.5 on 2020-06-29 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0004_amenity_facility_houserule'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='amenities',
            field=models.ManyToManyField(blank=True, to='rooms.Amenity'),
        ),
        migrations.AddField(
            model_name='room',
            name='facilities',
            field=models.ManyToManyField(blank=True, to='rooms.Facility'),
        ),
        migrations.AddField(
            model_name='room',
            name='house_rules',
            field=models.ManyToManyField(blank=True, to='rooms.HouseRule'),
        ),
        migrations.AlterField(
            model_name='room',
            name='room_type',
            field=models.ManyToManyField(blank=True, to='rooms.RoomType'),
        ),
    ]