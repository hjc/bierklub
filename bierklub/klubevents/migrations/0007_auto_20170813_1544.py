# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-13 19:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('klubevents', '0006_auto_20170727_1758'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='preamble',
            field=models.CharField(default='', max_length=1024),
        ),
    ]