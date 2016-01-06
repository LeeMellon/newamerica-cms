# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailcore.fields
import wagtail.wagtailembeds.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20160104_2146'),
        ('wagtailcore', '0020_add_index_on_page_first_published_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllPodcastsHomePage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
            ],
            options={
                'verbose_name': 'Homepage for all Podcasts',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='Podcast',
            fields=[
                ('post_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='home.Post')),
                ('soundcloud_embed', wagtail.wagtailcore.fields.StreamField([(b'soundcloud_embed', wagtail.wagtailembeds.blocks.EmbedBlock())])),
            ],
            options={
                'abstract': False,
            },
            bases=('home.post',),
        ),
        migrations.CreateModel(
            name='ProgramPodcastsPage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
            ],
            options={
                'verbose_name': 'Podcast Homepage for Program',
            },
            bases=('wagtailcore.page',),
        ),
    ]
