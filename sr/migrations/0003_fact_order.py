# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-30 01:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sr', '0002_memory'),
    ]

    operations = [
        migrations.AddField(
            model_name='fact',
            name='order',
            field=models.IntegerField(default=1, unique=True),
            preserve_default=False,
        ),
    ]