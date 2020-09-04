import dash
#import dash_core_components as dcc
import dash_html_components as html
import dash_table
from django_plotly_dash import DjangoDash
import pandas as pd
from django.conf import settings
from oss.models import Site, Instrument, Telescope, FacilityStatus

def format_link_entry(link_text, url):
    if 'None' in url:
        return 'All instruments'
    else:
        return f"["+link_text+"]("+url+")"

class TelescopeStatus():
    def __init__(self):
        self.site = None
        self.site_id = None
        self.telescope = None
        self.telescope_id = None
        self.instrument = None
        self.instrument_id = None
        self.status = None
        self.comment = None

    def get_status(self, telescope=None, instrument=None):
        status = None
        if telescope:
            try:
                status = FacilityStatus.objects.filter(telescope=telescope).latest('last_updated')
            except FacilityStatus.DoesNotExist:
                pass
        elif instrument:
            try:
                status = FacilityStatus.objects.filter(instrument=instrument).latest('last_updated')
            except FacilityStatus.DoesNotExist:
                pass

        if status:
            self.status = status.status
            self.comment = status.comment
        else:
            self.status = 'Unknown'
            self.comment = ''

def get_facility_status():

    tel_states = []

    status_data = FacilityStatus.objects.all()

    telescopes = Telescope.objects.all()
    for tel in telescopes:
        status = TelescopeStatus()
        status.site = tel.site.name
        status.site_id = tel.site.pk
        status.telescope = tel.name
        status.telescope_id = tel.pk
        status.get_status(telescope=tel)
        tel_states.append(status)

        cameras = Instrument.objects.filter(telescope=tel)
        for camera in cameras:
            status = TelescopeStatus()
            status.site = tel.site.name
            status.site_id = tel.site.pk
            status.telescope = tel.name
            status.telescope_id = tel.pk
            status.get_status(instrument=camera)
            tel_states.append(status)

    return tel_states

app = DjangoDash('FacilitiesTable')

table_columns = [dict(name='Site', id='Site', type='text', presentation='markdown'),
                 dict(name='Facility', id='Facility', type='text', presentation='markdown'),
                 dict(name='Instrument', id='Instrument', type='text', presentation='markdown'),
                 dict(name='Status', id='Status'),
                 dict(name='Comment', id='Comment')]

status_list = get_facility_status()

table_data = []
if status_list:
    for tel_status in status_list:
        table_data.append( dict(Site=format_link_entry(tel_status.site, '/site/'+str(tel_status.site_id)+'/'),
                             Facility=format_link_entry(tel_status.telescope, '/telescope/'+str(tel_status.telescope_id)+'/'),
                             Instrument=format_link_entry(tel_status.instrument, '/instrument/'+str(tel_status.instrument_id)+'/'),
                             Status=tel_status.status,
                             Comment=tel_status.comment) )

app.layout = html.Div( dash_table.DataTable(
            id='FacilitiesTable',
            columns=table_columns,
            data=table_data,
            sort_action="native",
            filter_action="native",
            style_table={'height': '600px', 'overflowY': 'auto'},
            style_cell={'fontSize':18, 'font-family':'sans-serif'},
            style_cell_conditional=[
                                {  'if': {'column_id': 'Status'},
                                    'backgroundColor': 'white',
                                    'color': 'black' },
                                {  'if': {'column_id': 'Status',
                                              'filter_query': '{Status} = "Offline"'},
                                        'backgroundColor': 'rgb(83, 7, 105)',
                                        'color': 'white' },
                                {  'if': {'column_id': 'Status',
                                          'filter_query': '{Status} = "Open"'},
                                    'backgroundColor': 'rgb(50, 168, 82)',
                                    'color': 'white' },
                                {  'if': {'column_id': 'Status',
                                          'filter_query': '{Status} = "Closed-weather"'},
                                    'backgroundColor': 'rgb(26, 80, 196)',
                                    'color': 'white' },
                                {  'if': {'column_id': 'Status',
                                          'filter_query': '{Status} = "Closed-unsafe"'},
                                    'backgroundColor': 'rgb(224, 132, 40)',
                                    'color': 'white' },
                                {  'if': {'column_id': 'Status',
                                          'filter_query': '{Status} = "Closed-daytime"'},
                                    'backgroundColor': 'rgb(218, 224, 40)',
                                    'color': 'white' },
                                {  'if': {'column_id': 'Status',
                                          'filter_query': '{Status} = "Unknown"'},
                                    'backgroundColor': 'rgb(168, 160, 160)',
                                    'color': 'white' },
                                {   'if': {
                                        'column_id': 'Status'  # 'text' | 'any' | 'datetime' | 'numeric'
                                    },
                                    'textAlign': 'left'},
                                {   'if': {
                                        'column_id': 'Comment'  # 'text' | 'any' | 'datetime' | 'numeric'
                                    },
                                    'textAlign': 'left'},
                            ],
            ) )
