# Generated by Django 2.2.5 on 2020-07-02 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0013_auto_20200702_0014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=models.ImageField(upload_to='room_photos'),
        ),
    ]
