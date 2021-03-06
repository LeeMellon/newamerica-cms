from django.db import models

from home.models import Post

from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core.blocks import URLBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel

from newamericadotorg.helpers import paginate_results, get_program_and_subprogram_posts, get_org_wide_posts
from programs.models import AbstractContentPage

class PolicyPaper(Post):
    """
    Policy paper class that inherits from the abstract
    Post model and creates pages for Policy Papers.
    """
    parent_page_types = ['ProgramPolicyPapersPage']
    subpage_types = []

    publication_cover_image = models.ForeignKey(
        'home.CustomImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    paper_url = StreamField([
        ('policy_paper_url', URLBlock(required=False, null=True)),
    ], null=True, blank=True)

    attachment = StreamField([
        ('attachment', DocumentChooserBlock(required=False, null=True)),
    ], null=True, blank=True)

    content_panels = Post.content_panels + [
        StreamFieldPanel('paper_url'),
        StreamFieldPanel('attachment'),
        ImageChooserPanel('publication_cover_image'),
    ]

    def get_context(self, request):
        context = super(PolicyPaper, self).get_context(request);
        for block in self.body:
            if block.block_type == 'panels':
                context['panels'] = block.value;
        return context;

    class Meta:
        verbose_name = 'Policy Paper'

class AllPolicyPapersHomePage(Page):
    """
    A page which inherits from the abstract Page model and
    returns every Policy Paper in the Policy Paper model
    for the organization wide Policy Paper Homepage
    """
    parent_page_types = ['home.Homepage']
    subpage_types = []

    @property
    def content_model(self):
        return PolicyPaper

    class Meta:
        verbose_name = "Homepage for all Policy Papers"


class ProgramPolicyPapersPage(AbstractContentPage):
    """
    A page which inherits from the abstract Page model and
    returns all Policy Papers associated with a specific
    Program or Subprogram
    """
    parent_page_types = ['programs.Program', 'programs.Subprogram', 'programs.Project']
    subpage_types = ['PolicyPaper']

    @property
    def content_model(self):
        return PolicyPaper

    class Meta:
        verbose_name = "Policy Papers Homepage"
