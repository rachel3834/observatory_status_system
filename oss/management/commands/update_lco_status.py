from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from oss.models import Telescope, FacilityStatus
from oss.management.commands import lco, ingest_utils
from dateutil.parser import parse as date_parser
from datetime import datetime
import pytz

class Command(BaseCommand):
    args = ''
    help = ''

    def _update_status_whole_network(self):
        network_status = lco.fetch_lco_telescope_states()
        lco_tel_codes = lco.get_lco_tel_codes()
        ts_now = datetime.utcnow()
        ts_now = ts_now.replace(tzinfo=pytz.UTC)

        for tel_code in lco_tel_codes:
            tel = self.get_lco_telescope(tel_code)

            if tel_code in network_status.keys():
                params = network_status[tel_code][0]

                tel_status = self.parse_status_data(params)

                status = FacilityStatus.objects.create(telescope=tel,
                                                        status=tel_status['state'],
                                                        status_start=tel_status['ts_start'],
                                                        status_end=tel_status['ts_end'],
                                                        comment=tel_status['comment'],
                                                        last_updated=ts_now)

                print('Recorded status for '+tel.name+' of '+str(tel_status['state']))

            else:
                comment = 'No status information provided'
                status = FacilityStatus.objects.create(telescope=tel,
                                                        status='Offline',
                                                        status_start=ts_now,
                                                        comment=comment,
                                                        last_updated=ts_now)

                print('No status information available for '+tel.name+' recording as offline')

    def get_lco_telescope(self, tel_code):
        qs = Telescope.objects.filter(tel_code=tel_code)
        (tel,message) = ingest_utils.test_qs_unique_result(qs, [tel_code])

        if message == 'OK':
            return tel
        else:
            raise IOError(message)

    def parse_status_data(self, params):

        status = {}
        status['comment'] = params['event_reason']
        status['ts_start'] = date_parser(params['start'])
        #status['ts_start'] = status['ts_start'].replace(tzinfo=pytz.UTC)
        status['ts_end'] = date_parser(params['end'])
        #status['ts_end'] = status['ts_end'].replace(tzinfo=pytz.UTC)

        if params['event_type'] == 'AVAILABLE':
            status['state'] = 'Open'
        elif params['event_type'] == 'NOT_OK_TO_OPEN' and \
            'Weather' in params['event_reason']:
            status['state'] = 'Closed-weather'
        elif params['event_type'] == 'NOT_OK_TO_OPEN' and \
            'Weather' not in params['event_reason']:
            status['state'] = 'Closed-unsafe-to-observe'
        elif params['event_type'] == 'ENCLOSURE_INTERLOCK':
            if 'WEATHER' in params['event_reason']:
                status['state'] = 'Closed-weather'
            else:
                status['state'] = 'Offline'
        elif params['event_type'] in ['SEQUENCER_DISABLED', 'SITE_AGENT_UNRESPONSIVE',\
                                        'ENCLOSURE_DISABLED', 'NOT_AVAILABLE']:
            status['state'] = 'Offline'
        else:
            status['state'] = 'Unknown'

        return status

    def handle(self,*args, **options):
        self._update_status_whole_network()
