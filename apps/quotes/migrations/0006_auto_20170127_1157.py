# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-27 19:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0005_auto_20170127_1156'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fav_quotes',
            name='quotes',
        ),
        migrations.AddField(
            model_name='fav_quotes',
            name='quotes',
            field=models.ManyToManyField(to='quotes.Quotes'),
        ),
    ]
