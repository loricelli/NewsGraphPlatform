# Generated by Django 3.0.6 on 2020-05-14 09:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('node', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Edge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(default='#000000', max_length=7)),
                ('stance', models.IntegerField(default=-1)),
                ('head', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='head', to='node.Node')),
                ('tail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tail', to='node.Node')),
            ],
        ),
    ]
