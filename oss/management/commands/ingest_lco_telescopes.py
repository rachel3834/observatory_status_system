from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from oss.models import Site, Installation, Telescope
from oss.management.commands import lco, ingest_utils

class Command(BaseCommand):
    args = ''
    help = ''

    def _ingest_telescopes(self):
        tel_list = lco.fetch_lco_telescopes()
        operator = User.objects.filter(username='rstreet1')[0]

        for tel in tel_list:
            qs = Site.objects.filter(site_code=tel['site_code'])
            (site, message) = ingest_utils.test_qs_unique_result(qs, [tel['site_code']])

            if message == 'OK':
                qs = Installation.objects.filter(name=tel['installation'],
                                                            site=site)
                (installation,message2) = ingest_utils.test_qs_unique_result(qs, [tel['site_code'],site.name])

                if message2 == 'OK':
                    (new_tel, ingested) = Telescope.objects.get_or_create(name=tel['name'],
                                                          tel_code=tel['tel_code'],
                                                          aperture=tel['aperture'],
                                                          operator=operator,
                                                          site=site,
                                                          installation=installation,
                                                          url=tel['url'])
                    print('Ingested telescope '+tel['name']+' at '+site.name)

                else:
                    print(message2)

            else:
                print(message)

    def handle(self,*args, **options):
        self._ingest_telescopes()
