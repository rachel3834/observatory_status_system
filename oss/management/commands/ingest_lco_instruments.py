from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from oss.models import Site, Installation, Telescope, FacilityOperator
from oss.models import Instrument, InstrumentCapabilities
from oss.management.commands import lco

class Command(BaseCommand):
    args = ''
    help = ''

    def _ingest_telescopes(self):
        instrument_list = lco.fetch_lco_instruments()
        operator = FacilityOperator.objects.filter(name='Las Cumbres Observatory')[0]

        for instrument in instrument_list:

            (site_code, enclosure, tel_id) = instrument['site_code'].split('.')
            site_name = lco.parse_site_code(site_code)
            qs = Site.objects.filter(name=site_name)

            if len(qs) == 1:
                site = qs[0]

                qs = Telescope.objects.filter(name=instrument['site_code'])

                if len(qs) == 1:
                    tel = qs[0]
                    (new_instrument, ingested) = Instrument.objects.get_or_create(name=instrument['name'],
                                                            wavelength=instrument['wavelength'],
                                                            telescope=tel)

                    for capability in instrument['capabilities']:
                        qs = InstrumentCapabilities.objects.filter(descriptor=capability)
                        if len(qs) == 1:
                            new_instrument.capabilities.add(qs[0])
                        elif len(qs) > 1:
                            raise IOError('Ambiguous instrument capability '+capability)
                        elif len(qs) == 0:
                            raise IOError('Unrecognised instrument capability '+capability)

                    print('Ingested new telescope '+new_instrument.name)
                    
                elif len(qs) == 0:
                    raise IOError('Unrecognised telescope code indicated: '+instrument['site_code'])
                elif len(qs) > 1:
                    raise IOError('Ambiguous telescope code indicated: '+instrument['site_code'])

            elif len(qs) == 0:
                raise IOError('Unrecognised site code indicated: '+site_code+' '+site_name)
            elif len(qs) > 1:
                raise IOError('Ambiguous site code indicated: '+site_code+' '+site_name)

    def handle(self,*args, **options):
        self._ingest_telescopes()
