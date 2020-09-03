import dash
#import dash_core_components as dcc
import dash_html_components as html
import dash_table
from django_plotly_dash import DjangoDash
import pandas as pd
from importlib import import_module
from django.conf import settings

def format_link_entry(link_text, url):
    return f"["+link_text+"]("+url+")"

app = DjangoDash('FacilitiesTable')

table_columns = [dict(name='Site', id='Site', type='text', presentation='markdown'),
                 dict(name='Facility', id='Facility', type='text', presentation='markdown'),
                 dict(name='Instrument', id='Instrument', type='text', presentation='markdown'),
                 dict(name='Status', id='Status'),
                 dict(name='Comment', id='Comment')]

client_module = import_module('api_client')
client = getattr(client_module, 'OSSAPIClient')

site_states = client.get_facility_status()

table_data = []
for site_name, tel_states in site_states.items():
    for tel_status in tel_states:
        for instrument in tel_status.instruments:
            table_data.append( dict(Site=format_link_entry(site_name, '/site/'+str(tel_status.site.pk)+'/'),
                                 Facility=format_link_entry(tel_status.name, '/telescope/'+str(tel_status.telescope.pk)+'/'),
                                 Instrument=format_link_entry(instrument[0], '/instrument/'+str(instrument[3])+'/'),
                                 Status=tel_status.status, #-> instrument[1],
                                 Comment=instrument[2]) )

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
                            ],
            ) )
