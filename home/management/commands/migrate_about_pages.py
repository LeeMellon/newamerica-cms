from django.core.management.base import BaseCommand
from wagtail.core.models import Page
from programs.models import Program, Subprogram, FeaturedProgramPage, FeaturedSubprogramPage
from home.models import ProgramAboutPage, ProgramAboutHomePage, Page
from wagtail.contrib.redirects.models import Redirect

class Command(BaseCommand):
    def handle(self, *args, **options):
        programs = Program.objects.all()
        subprograms = Subprogram.objects.all()

        publish_new_program_about_pages(self, programs)
        publish_new_program_about_pages(self, subprograms, False)

def delete_new_about_home_pages():
    ProgramAboutHomePage.objects.all().delete()

def publish_new_program_about_pages(self, programs, with_sidebar=True):
    for p in programs:
        if not p.about_us_page:
            continue

        a = p.about_us_page.specific
        slug = a.slug
        orig_url = a.url
        a.slug = a.slug.replace('_legacy', '') + '_legacy';
        a.unpublish()
        self.stdout.write('changed %s to %s' % (orig_url, a.slug))

        ahp = p.add_child(instance=ProgramAboutHomePage(
            title=a.title,
            slug='about',
            seo_title=a.seo_title,
            search_description=a.search_description,
            show_in_menus=True,
            story_image=a.story_image,
            body=a.body,
            story_excerpt=a.story_excerpt,
            data_project_external_script=a.data_project_external_script
        ))
        ahp.save()
        self.stdout.write('created %s' % ahp.url)

        if slug != 'about':
            Redirect(
                old_path=orig_url,
                redirect_page=ahp
            ).save()

            self.stdout.write('created redirect from %s to %s' % (orig_url, ahp.url))


        if not with_sidebar: continue
        self.stdout.write('searching for sidebar content...')
        about_pages = p.sidebar_menu_about_us_pages.stream_data
        for ap_stream_data in about_pages:
            ap = Page.objects.filter(id=ap_stream_data['value'])
            ap = ap.first()
            if not ap: continue
            self.stdout.write('found %s' % ap.url)
            if ap.title == 'About Us' or ap.title == 'Our People' or ap.title == 'About': continue
            ap = ap.specific

            new_ap = ahp.add_child(instance=ProgramAboutPage(
                title=ap.title,
                slug=ap.slug,
                search_description=ap.search_description,
                seo_title=ap.seo_title,
                show_in_menus=True,
                story_image=getattr(ap, 'story_image', None),
                body=getattr(ap, 'body', None),
                story_excerpt=getattr(ap, 'story_excerpt', None),
                data_project_external_script=getattr(ap, 'data_project_external_script', None)
            ))

            self.stdout.write('created %s' % new_ap.url)
            new_ap.save()
            new_ap.save_revision().publish()

            Redirect(
                old_path=ap.url,
                redirect_page=new_ap
            ).save()

            self.stdout.write('created redirect from %s to %s' % (ap.url, new_ap.url))

        a.unpublish()
        ahp.save_revision().publish()
