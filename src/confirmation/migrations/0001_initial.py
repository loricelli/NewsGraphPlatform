# Generated by Django 3.0.6 on 2020-05-14 09:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('voter', '0001_initial'),
        ('edge', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Confirmation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote', models.IntegerField()),
                ('edge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='edge.Edge')),
                ('voter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='voter.Voter')),
            ],
        ),
    ]