# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2018-03-27 21:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0007_auto_20180226_0804'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='publicationspage',
            options={'verbose_name': 'Publications Homepage'},
        ),
        migrations.AlterModelOptions(
            name='subprogram',
            options={'ordering': ('title',), 'verbose_name': 'Initiative/Project Homepage'},
        ),
    ]
