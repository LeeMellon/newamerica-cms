import json
import datetime
from home.models import Post
from django import forms
from django.db import models
from django.utils.text import slugify

from modelcluster.fields import ParentalKey, ParentalManyToManyField  

from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, StreamFieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField, StreamField
from wagtail.search import index

from programs.models import AbstractContentPage

from wagtailautocomplete.edit_handlers import AutocompletePanel
from multiselectfield import MultiSelectField

class ProgramSurveysPage(AbstractContentPage):
    parent_page_types = ['programs.Program', 'programs.Subprogram', 'programs.Project']
    subpage_types = ['Survey', 'Commentary', 'SurveyValuesIndex']

    @property
    def content_model(self):
        return Survey

    class Meta:
        verbose_name = "Surveys Homepage"

    def __str__(self):
        return self.title

class SurveyOrganization(Page):
    parent_page_types = ['SurveyValuesIndex', 'ProgramSurveysPage']
    subpage_type = []
    
    @classmethod
    def autocomplete_create(cls: type, value: str):
      test = ProgramSurveysPage.objects.first().title
    
      orgs_index_page = SurveyValuesIndex.objects.first()
      title = value

      new = cls(title=value)
      orgs_index_page.add_child(instance=new)
      orgs_index_page.save()
      return new

    def clean(self):
      """Override the values of title and slug before saving."""
      super().clean()
      if not self.slug:
        self.slug = slugify(self.title)   
  
    
    def __str__(self):
      return self.title
    class Meta:
        verbose_name_plural = 'Survey Organizations'



class DemographicKey(Page):
    parent_page_types = ['SurveyValuesIndex', 'ProgramSurveysPage']
    subpage_type = []
    
    @classmethod
    def autocomplete_create(cls: type, value: str):
      test = ProgramSurveysPage.objects.first().title
    
      orgs_index_page = SurveyValuesIndex.objects.first()
      title = value

      new = cls(title=value)
      orgs_index_page.add_child(instance=new)
      orgs_index_page.save()
      return new

    def clean(self):
      """Override the values of title and slug before saving."""
      super().clean()
      # self.title = '%s %s' % (self.lable)
      if not self.slug:
        self.slug = slugify(self.title)   

      def __str__(self):
        return self.title
    class Meta:
      verbose_name_plural = 'Demographic Keys'

class SurveyValuesIndex(Page):
    parent_page_types = ['ProgramSurveysPage']
    subpage_type = ['SurveyOrganization', 'DemographicKey']

    def get_orgs(self):
      return SurveyOrganization.objects.live().descendant_of(self)
  
    def get_context(self, request, *args, **kwargs):
      context = super(SurveyValuesIndex, self).get_context(request)

      orgs = self.get_orgs() 

      context['orgs'] = orgs

      return context

    @property
    def content_model(self):
        return SurveyOrganization

    def __str__(self):
        return self.title
    class Meta:
      verbose_name = "Surveyindex Homepage"

class Survey(Post, RoutablePageMixin):
    template = 'survey/survey.html'
    
    MONTH_CHOICES = (
      (0, 'N/A'),
      (1, 'January'),
      (2, 'February'),
      (3, 'March'),
      (4, 'April'),
      (5, 'May'),
      (6, 'June'),
      (7, 'July'),
      (8, 'August'),
      (9, 'September'),
      (10, 'October'),
      (11, 'November'),
      (12, 'December')
    )

    DATA_TYPE_CHOICES = (
      ('QUANT', 'Quantitative'),
      ('QUAL', 'Qualitative')
    )

    parent_page_types = ['ProgramSurveysPage']
    subpage_type=[]
    current_year = datetime.datetime.now().year

    study_title= models.CharField(max_length=250, blank=True, null=True)
    org = ParentalManyToManyField('SurveyOrganization', related_name='SurveyOrganization', blank=True)
    year = models.IntegerField(help_text='Year Survey was condicted.', blank=True, default=current_year)
    month = models.IntegerField(choices=MONTH_CHOICES, default=None, help_text='Month Survey was condicted, if applicable.')
    sample_number = models.CharField(max_length=250, blank=True, null=True)
    sample_demos = models.CharField(max_length=250, blank=True, null=True, help_text='Text displayed on the dashboard')
    demos_key = ParentalManyToManyField('DemographicKey', help_text='Indexable demographic groups', blank=True, default=False)
    data_type = MultiSelectField(choices=DATA_TYPE_CHOICES, default=['QUANT', 'QUAL'])  
    findings = RichTextField(blank=True, null=True, max_length=12500)
    link = models.URLField(blank=True, null=True)
    file = models.FileField(blank=True, null=True)
    assoc_commentary = ParentalManyToManyField('Commentary', blank=True, through='Commented_Survey', related_name='surveys')
    content_panels = [
      MultiFieldPanel([
        FieldPanel('date'),
      ], heading='Survey Created'),
      MultiFieldPanel([
        FieldPanel('title'),
        AutocompletePanel('org'),
        FieldPanel('year'),
        FieldPanel('month'),
        FieldPanel('sample_number'),
        FieldPanel('sample_demos'),
        AutocompletePanel('demos_key'),
        FieldPanel('data_type', widget=forms.CheckboxSelectMultiple),
        FieldPanel('findings'),
        AutocompletePanel('assoc_commentary')
      ], heading='Survey Data'),
      MultiFieldPanel([
        FieldPanel('link'),
        FieldPanel('file')
      ])
    ]

class Commentary(Post, RoutablePageMixin):
  template = 'survey/commentary.html'

  parent_page_types = ['ProgramSurveysPage']
  subpage_types = []

  assoc_surveys = ParentalManyToManyField('Survey', through='Commented_Survey', blank=True, related_name='commentaries')

  content_panels = [
      FieldPanel('title'),
      FieldPanel('subheading'),
      FieldPanel('date'),
      StreamFieldPanel('body'),
      InlinePanel('authors', label=("Authors")),
      InlinePanel('topics', label=("Topics")),
      AutocompletePanel('assoc_surveys')
  ]

  def __str__(self):
        return self.title
  class Meta:
      verbose_name = 'Expert Commentary'

class Commented_Survey(models.Model):
  survey=models.ForeignKey('Survey', on_delete=models.CASCADE, blank=True, null=True)
  commentary=models.ForeignKey('Commentary', on_delete=models.CASCADE, blank=True, null=True)