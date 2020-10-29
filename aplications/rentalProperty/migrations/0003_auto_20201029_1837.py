# Generated by Django 2.2.6 on 2020-10-29 21:37

import datetime
import django.core.validators
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('rentalProperty', '0002_auto_20201025_1654'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='pax',
            field=models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='property',
            name='maxPax',
            field=models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 10, 29, 21, 37, 53, 890259, tzinfo=utc)),
        ),
    ]
