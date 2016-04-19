from django.test import TestCase

from wagtail.tests.utils import WagtailPageTests
from wagtail.wagtailcore.models import Page

from .models import HomePage, OrgSimplePage, JobsPage, SubscribePage

from programs.models import Program

from weekly.models import Weekly

from article.models import AllArticlesHomePage, ProgramArticlesPage, Article

from event.models import AllEventsHomePage

from blog.models import AllBlogPostsHomePage

from book.models import AllBooksHomePage

from person.models import OurPeoplePage, BoardAndLeadershipPeoplePage

from podcast.models import AllPodcastsHomePage

from policy_paper.models import AllPolicyPapersHomePage

from press_release.models import AllPressReleasesHomePage

from quoted.models import AllQuotedHomePage


class HomeTests(WagtailPageTests):
    """
    Testing hierarchies between pages and whether it is possible 
    to create a Homepage and all the allowed subpages 
    underneath the Homepage.
    """

    def setUp(self):
        self.login()
        self.root_page = Page.objects.get(id=1)
        self.home_page = self.root_page.add_child(instance=HomePage(
            title='New America')
        )
        self.program_page = self.home_page.add_child(
            instance=Program(
                title='OTI',
                name='OTI',
                description='OTI',
                location=False,
                depth=3
            )
        )
        self.program_articles_page = self.program_page.add_child(
            instance=ProgramArticlesPage(title='Program Articles')
        )
        self.article = self.program_articles_page.add_child(
            instance=Article(
                title='Article 1', 
                date='2016-02-02'
            )
        )


    def test_can_create_homepage_under_root_page(self):
        parent_page = Page.get_first_root_node()
        home = HomePage(title='New America')
        parent_page.add_child(instance=home)

    #Test that a particular child Page type can be created under a parent Page type
    def test_can_create_program_articles_page_under_program(self):
        self.assertCanCreateAt(Page, HomePage)

    #Test that the only page types that can be created under parent_model are child_models
    def test_article_subpages(self):
        self.assertAllowedSubpageTypes(HomePage, {
            AllArticlesHomePage,
            AllBooksHomePage,
            AllBlogPostsHomePage,
            AllEventsHomePage,
            AllPodcastsHomePage,
            AllPolicyPapersHomePage,
            AllPressReleasesHomePage,
            AllQuotedHomePage,
            BoardAndLeadershipPeoplePage,
            JobsPage,
            OurPeoplePage, 
            OrgSimplePage,
            Program,
            SubscribePage,
            Weekly,
            })

    #Test that pages can be created with POST data
    def test_can_create_homepage_under_page(self):
        self.assertCanCreate(self.root_page, HomePage, {
            'title':'New America 2',
            'slug': 'new-america-2',
            'recent_carousel-count': 0,
            }
        )

    def test_can_create_program_under_homepage(self):
        self.assertCanCreate(self.home_page, Program, {
            'title':'OTI2',
            'name': 'OTI2',
            'description': 'OTI2',
            'slug': 'oti-2',
            'depth': 3,
            'feature_carousel-count': 0,
            'sidebar_menu_initiatives_and_projects_pages-count': 0,
            'sidebar_menu_our_work_pages-count': 0,
            'sidebar_menu_about_us_pages-count': 0,
            }
        )

    def test_adding_lead_story_to_homepage(self):
        self.home_page.lead_1 = self.article
        self.home_page.save()
        self.assertEqual(self.home_page.lead_1, self.article)

    def test_adding_feature_story_to_homepage(self):
        self.home_page.feature_1 = self.article
        self.home_page.save()
        self.assertEqual(self.home_page.feature_1, self.article)

    def test_adding_story_to_homepage_recent_carousel(self):
        self.home_page.recent_carousel.stream_data.append(
            {
                'type': 'event',
                'value': self.article.id
            }
        )
        self.assertEqual(
            self.home_page.recent_carousel.stream_data[0]['value'], 
            self.article.id
        )
