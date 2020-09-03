import dash
#import dash_core_components as dcc
import dash_html_components as html
import dash_table
from django_plotly_dash import DjangoDash
import pandas as pd
from django.conf import settings
from . import api_client

def format_link_entry(link_text, url):
    if 'None' in url:
        return 'All instruments'
    else:
        return f"["+link_text+"]("+url+")"

app = DjangoDash('FacilitiesTable')

table_columns = [dict(name='Site', id='Site', type='text', presentation='markdown'),
                 dict(name='Facility', id='Facility', type='text', presentation='markdown'),
                 dict(name='Instrument', id='Instrument', type='text', presentation='markdown'),
                 dict(name='Status', id='Status'),
                 dict(name='Comment', id='Comment')]

client = api_client.OSSAPIClient()
status_list = client.get_facility_status(settings.DEPLOYED_URL+'/facility_status/')

table_data = []
if status_list:
    for tel_status in status_list:
        table_data.append( dict(Site=format_link_entry(tel_status['site'], '/site/'+str(tel_status['site_id'])+'/'),
                             Facility=format_link_entry(tel_status['telescope'], '/telescope/'+str(tel_status['telescope_id'])+'/'),
                             Instrument=format_link_entry(tel_status['instrument'], '/instrument/'+str(tel_status['instrument_id'])+'/'),
                             Status=tel_status['status'],
                             Comment=tel_status['comment']) )

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
