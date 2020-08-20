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
            qs = Telescope.objects.filter(tel_code=instrument['tel_code'])
            (tel, message) = ingest_utils.test_qs_unique_result(qs, [instrument['tel_code']])

            if message == 'OK':
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

                print('Ingested instrument '+instrument['name']+' at '+instrument['tel_code'])
                
            else:
                print(message)


    def handle(self,*args, **options):
        self._ingest_telescopes()
