# Generated by Django 3.0.7 on 2020-12-18 23:41

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import multiselectfield.db.fields
import wagtail.contrib.routable_page.models
import wagtail.core.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('home', '0054_auto_20200810_1541'),
    ]

    operations = [
        migrations.CreateModel(
            name='Commentary',
            fields=[
                ('post_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='home.Post')),
            ],
            options={
                'verbose_name': 'Expert Commentary',
            },
            bases=('home.post', wagtail.contrib.routable_page.models.RoutablePageMixin),
        ),
        migrations.CreateModel(
            name='Commented_Survey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commentary', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='survey.Commentary')),
            ],
        ),
        migrations.CreateModel(
            name='DemographicKey',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
            ],
            options={
                'verbose_name_plural': 'Demographic Keys',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='SurveyOrganization',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
            ],
            options={
                'verbose_name_plural': 'Survey Organizations',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='SurveyTags',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
            ],
            options={
                'verbose_name_plural': 'Survey Tags',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='SurveyValuesIndex',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
            ],
            options={
                'verbose_name': 'Surveyindex Homepage',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('post_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='home.Post')),
                ('year', models.IntegerField(blank=True, default=2000, help_text='Year Survey was conducted.')),
                ('month', models.IntegerField(choices=[(0, 'N/A'), (1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')], default=None, help_text='Month Survey was conducted, if applicable.')),
                ('sample_number', models.IntegerField(blank=True, null=True)),
                ('sample_demos', models.CharField(blank=True, help_text='Text displayed on the dashboard', max_length=250, null=True, verbose_name='Sample Demographics')),
                ('findings', wagtail.core.fields.RichTextField(blank=True, max_length=12500, null=True)),
                ('data_type', multiselectfield.db.fields.MultiSelectField(choices=[('QUANT', 'Quantitative'), ('QUAL', 'Qualitative')], max_length=10)),
                ('national', models.BooleanField(default=True, help_text='Indicates whether the survey was nationally representative or not.', verbose_name='Nationally Representative?')),
                ('link', models.URLField(blank=True, help_text='Add a link to a webpage containing the survey details.', null=True, verbose_name='Link to Survey')),
                ('file', models.FileField(blank=True, help_text='Add a file containing the survey details.', null=True, upload_to='', verbose_name='Survey File')),
                ('assoc_commentary', modelcluster.fields.ParentalManyToManyField(blank=True, related_name='surveys', through='survey.Commented_Survey', to='survey.Commentary', verbose_name='Associated Commentary')),
                ('demos_key', modelcluster.fields.ParentalManyToManyField(blank=True, default=False, help_text='Indexable demographic groups', to='survey.DemographicKey', verbose_name='Demographics Keys')),
                ('org', modelcluster.fields.ParentalManyToManyField(blank=True, related_name='SurveyOrganization', to='survey.SurveyOrganization', verbose_name='Organization')),
                ('tags', modelcluster.fields.ParentalManyToManyField(blank=True, default=False, help_text='Select from available tags', to='survey.SurveyTags', verbose_name='Topics')),
            ],
            options={
                'abstract': False,
            },
            bases=('home.post',),
        ),
        migrations.CreateModel(
            name='ProgramSurveysPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('subheading', models.CharField(blank=True, max_length=200)),
                ('about', wagtail.core.fields.RichTextField(blank=True, max_length=1500, verbose_name='About This Project')),
                ('methodology', wagtail.core.fields.RichTextField(blank=True, max_length=1500)),
                ('partner_logo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='home.CustomImage')),
            ],
            options={
                'verbose_name': 'Surveys Homepage',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.AddField(
            model_name='commented_survey',
            name='survey',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='survey.Survey'),
        ),
        migrations.AddField(
            model_name='commentary',
            name='assoc_surveys',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, related_name='commentaries', through='survey.Commented_Survey', to='survey.Survey'),
        ),
    ]