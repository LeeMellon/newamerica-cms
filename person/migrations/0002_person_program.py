# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0001_initial'),
        ('programs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='program',
            field=models.ForeignKey(to='programs.Program', blank=True, null=True),
        ),
    ]
