# Generated by Django 3.1.7 on 2021-06-07 21:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Patient', '0003_prescription'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor_latest_diagnosis',
            name='valid_until',
            field=models.DateField(default=datetime.date.today, verbose_name='Date'),
        ),
    ]
