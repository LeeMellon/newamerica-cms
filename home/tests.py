from django.test import TestCase

from wagtail.tests.utils import WagtailPageTests
from wagtail.wagtailcore.models import Page

from .models import HomePage


class HomeTests(WagtailPageTests):
	
	def test_can_create_homepage(self):
		parent_page = Page.get_first_root_node()
		home = HomePage(title='New America')
		parent_page.add_child(instance=home)