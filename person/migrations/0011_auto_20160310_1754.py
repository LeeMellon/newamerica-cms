# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-03-10 17:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0010_auto_20160310_0442'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='position_at_new_america',
            field=models.CharField(blank=True, help_text=b'Position or Title at New America', max_length=500, null=True),
        ),
    ]