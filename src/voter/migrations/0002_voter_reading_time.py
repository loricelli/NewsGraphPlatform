# Generated by Django 3.0.6 on 2020-05-19 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voter', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='voter',
            name='reading_time',
            field=models.IntegerField(default=0),
        ),
    ]
