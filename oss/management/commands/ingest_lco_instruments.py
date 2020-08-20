from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from oss.models import Site, Installation, Telescope, FacilityOperator
from oss.models import Instrument, InstrumentCapabilities
from oss.management.commands import lco, ingest_utils

class Command(BaseCommand):
    args = ''
    help = ''

    def _ingest_telescopes(self):
        instrument_list = lco.fetch_lco_instruments()
        operator = FacilityOperator.objects.filter(name='Las Cumbres Observatory')[0]

        for instrument in instrument_list:

            qs = Site.objects.filter(site_code=instrument['site_code'])
            (site, message) = ingest_utils.test_qs_unique_result(qs, [instrument['site_code']])

            if message == 'OK':
                qs = Installation.objects.filter(name=instrument['installation'],
                                                                site=site)
                (installation,message2) = ingest_utils.test_qs_unique_result(qs, [instrument['site_code'],site.name])

                if message2 == 'OK':
                    qs = Telescope.objects.filter(name=instrument['telescope'],
                                                        site=site,
                                                        installation=installation)
                                                        
                    (tel, message3) = ingest_utils.test_qs_unique_result(qs, [instrument['site_code'],site.name, installation.name])

                    if message3 == 'OK':
                        (new_instrument, stat) = Instrument.objects.get_or_create(name=instrument['name'],
                                                                          telescope=tel,
                                                                          wavelength=instrument['wavelength'])

                        for capability in instrument['capabilities']:
                            qs = InstrumentCapabilities.objects.filter(descriptor=capability)
                            if len(qs) == 0:
                                cap = InstrumentCapabilities.create(descriptor=capability)
                            else:
                                cap = qs[0]

                            new_instrument.capabilities.add(cap)
                            new_instrument.save()

                    else:
                        print(message3)

                else:
                    print(message2)

            else:
                print(message)


    def handle(self,*args, **options):
        self._ingest_telescopes()
