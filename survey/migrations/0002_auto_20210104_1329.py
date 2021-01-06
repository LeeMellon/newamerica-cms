# Generated by Django 3.0.7 on 2021-01-04 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='description',
            field=models.CharField(blank=True, help_text='A brief description of the survey. 500 chars max', max_length=500, null=True),
        ),
    ]