from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from oss.models import Site
from oss.management.commands import lco

class Command(BaseCommand):
    args = ''
    help = ''

    def _ingest_sites(self):
        sites_list = lco.fetch_lco_sites()

        for site in sites_list:
            (new_site, stat) = Site.objects.get_or_create(name=site['name'],
                                                  location=site['location'],
                                                  latitude=site['latitude'],
                                                  longitude=site['longitude'],
                                                  altitude=site['altitude'],
                                                  site_code=site['site_code'],
                                                  url=site['url'])

            print('Created site '+repr(new_site))

    def handle(self,*args, **options):
        self._ingest_sites()
