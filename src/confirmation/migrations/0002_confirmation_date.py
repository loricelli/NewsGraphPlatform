# Generated by Django 3.0.6 on 2020-05-18 07:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('confirmation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='confirmation',
            name='date',
            field=models.DateTimeField(default=datetime.datetime.now, editable=False),
        ),
    ]