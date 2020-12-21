# Generated by Django 3.0.7 on 2020-12-21 20:09

from django.conf import settings
from django.db import migrations
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('home', '0055_auto_20201218_1414'),
        ('wagtailredirects', '0006_redirect_increase_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wagtailcore', '0055_auto_20201218_1812'),
        ('wagtailforms', '0004_add_verbose_name_plural'),
        ('survey', '0004_auto_20201218_1636'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ProgramSurveysPage',
            new_name='SurveysHomePage',
        ),
        migrations.AddField(
            model_name='survey',
            name='description',
            field=wagtail.core.fields.RichTextField(blank=True, help_text='A brief description of the survey.', max_length=500, null=True),
        ),
    ]
