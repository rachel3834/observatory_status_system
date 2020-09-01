from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from oss.models import Installation, Site, FacilityOperator
from oss.management.commands import lco, ingest_utils

class Command(BaseCommand):
    args = ''
    help = ''

    def _ingest_sites(self):
        installation_list = lco.fetch_lco_installations()

        for installation in installation_list:
            qs = Site.objects.filter(site_code=installation['site_code'])

            (site, message) = ingest_utils.test_qs_unique_result(qs, [installation['site_code']])

            if message == 'OK':
                (new_install, stat) = Installation.objects.get_or_create(name=installation['name'],
                                                                        type=installation['type'],
                                                                        site=site)
                print('Created installation '+repr(new_install)+' at site '+site.name)

            else:
                print(message)

    def handle(self,*args, **options):
        self._ingest_sites()
