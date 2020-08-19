from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from oss.models import Site, Installation, Telescope, FacilityOperator
from oss.management.commands import lco

class Command(BaseCommand):
    args = ''
    help = ''

    def _ingest_telescopes(self):
        instrument_list = lco.fetch_lco_instruments()
        operator = FacilityOperator.objects.filter(name='Las Cumbres Observatory')[0]

        for instrument in instrument_list:

            (site_id, enclosure, tel_id) = instrument['site_code'].split('.')
            site_name = lco.parse_site_code(site_id)
            qs = Site.objects.filter(name=site_name)

            if len(qs) == 1:
                (new_dome,ingested) = Installation.objects.get_or_create(name='lco_'+site_id+'_'+enclosure,
                                                            type='Dome', site=qs[0])
                print('Ingested installation '+'lco_'+site_id+'_'+enclosure+' type=Dome site='+repr(qs[0]))

                aperture = lco.parse_aperture_from_telid(tel_id)
                (new_tel, ingested) = Telescope.objects.get_or_create(name=instrument['site_code'],
                                                          aperture=aperture,
                                                          operator=operator,
                                                          site=qs[0],
                                                          installation=new_dome)
                print('Ingested new telescope '+new_tel.name)

            elif len(qs) == 0:
                raise IOError('Unrecognised site code indicated: '+site_code+' '+site_name)
            elif len(qs) > 1:
                raise IOError('Ambiguous site code indicated: '+site_code+' '+site_name)

    def handle(self,*args, **options):
        self._ingest_telescopes()
