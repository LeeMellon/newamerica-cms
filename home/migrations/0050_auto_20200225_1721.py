# -*- coding: utf-8 -*-
# Generated by Django 1.11.27 on 2020-02-25 22:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0049_auto_20200207_2032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='ordered_date_string',
            field=models.CharField(max_length=140),
        ),
    ]