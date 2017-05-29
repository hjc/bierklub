# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-29 16:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=4096)),
                ('date', models.DateTimeField()),
                ('number', models.IntegerField(verbose_name='number IRT total events')),
                ('location', models.CharField(max_length=128, verbose_name='address of brewery')),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='full name')),
                ('email', models.EmailField(max_length=254)),
                ('join_date', models.DateField()),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='attendees',
            field=models.ManyToManyField(db_table='klubevents_event_members', to='klubevents.Member'),
        ),
    ]