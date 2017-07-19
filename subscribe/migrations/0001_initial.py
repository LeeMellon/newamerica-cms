# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-07-19 16:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0032_add_bulk_delete_page_permission'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubscribePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
            ],
            options={
                'verbose_name': 'New America Mailing List',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='SubscriptionSegment',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('SegmentID', models.TextField()),
                ('ListID', models.TextField()),
            ],
            options={
                'verbose_name': 'Mailing List Segment',
            },
            bases=('wagtailcore.page',),
        ),
    ]
