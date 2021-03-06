# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-21 20:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Airport',
            fields=[
                ('code', models.CharField(max_length=3, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Carrier',
            fields=[
                ('code', models.CharField(max_length=3, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Flights',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cancelled', models.IntegerField()),
                ('on_time', models.IntegerField()),
                ('total', models.IntegerField()),
                ('delayed', models.IntegerField()),
                ('diverted', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='MinutesDelayed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('late_aircraft', models.IntegerField()),
                ('weather', models.IntegerField()),
                ('carrier', models.IntegerField()),
                ('security', models.IntegerField()),
                ('total', models.IntegerField()),
                ('nat_avi_sys', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='NumDelays',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weather', models.IntegerField()),
                ('security', models.IntegerField()),
                ('late_aircraft', models.IntegerField()),
                ('nat_avi_sys', models.IntegerField()),
                ('carrier', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Statistics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flights', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='airports.Flights')),
                ('minutes_del', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='airports.MinutesDelayed')),
                ('num_del', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='airports.NumDelays')),
            ],
        ),
        migrations.CreateModel(
            name='StatisticsGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('airport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='airports.Airport')),
                ('carrier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='airports.Carrier')),
                ('statistics', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='airports.Statistics')),
            ],
        ),
        migrations.CreateModel(
            name='Time',
            fields=[
                ('label', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('year', models.IntegerField()),
                ('month', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='statisticsgroup',
            name='time',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='airports.Time'),
        ),
    ]
