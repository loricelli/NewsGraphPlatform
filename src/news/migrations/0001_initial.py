# Generated by Django 3.0.6 on 2020-05-14 09:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('source', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('news_id', models.IntegerField()),
                ('title', models.TextField()),
                ('body', models.TextField(blank=True, null=True)),
                ('publish_date', models.DateTimeField(auto_now_add=True)),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='source.Source')),
            ],
        ),
    ]
