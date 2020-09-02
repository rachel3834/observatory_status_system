from django import template
from django.conf import settings
import dash
#import dash_core_components as dcc
import dash_html_components as html
import dash_table
from django_plotly_dash import DjangoDash
import pandas as pd

register = template.Library()

STATUS_MAP = {'Closed-weather': {'bgcolor': '#0349fc', 'fontcolor': '#ffffff'},
              'Open': {'bgcolor': '#00d620', 'fontcolor': '#ffffff'},
              'Offline': {'bgcolor': '#d65900', 'fontcolor': '#ffffff'},
              'Unknown': {'bgcolor': '#ffffff', 'fontcolor': '#000000'}}

def color_code_telescope_status(tel_status):
    """
    Formats the display of the facility's status information
    """

    tel_bgcolor = STATUS_MAP[tel_status.status]['bgcolor']
    tel_fontcolor = STATUS_MAP[tel_status.status]['fontcolor']

    bgcolors = []
    fontcolors = []

    instruments = []
    for instrument in tel_status.instruments:
        bg = STATUS_MAP[instrument[1]]['bgcolor']
        font = STATUS_MAP[instrument[1]]['fontcolor']
        instruments.append( list(instrument) + [bg, font] )

    #print(instruments)
    return {'tel_status': tel_status,
            'tel_bgcolor': tel_bgcolor, 'tel_fontcolor': tel_fontcolor,
            'instruments': instruments}


@register.inclusion_tag('oss/partials/facility_list_entry.html')
def telescope_status_entry(tel_status):
    """
    Formats the display of the facility's status information in
    the main facilities list table
    """
    context = color_code_telescope_status(tel_status)
    return context


@register.inclusion_tag('oss/partials/telescope_site_entry.html')
def telescope_site_entry(tel_status):
    """
    Formats the display of the facility's status information in
    the list of facilities at a single site
    """
    context = color_code_telescope_status(tel_status)
    context['tel_id'] = tel_status.telescope.pk
    return context

def format_link_entry(link_text, url):
    return f"["+link_text+"]("+url+")"

def build_facilities_datatable(table_columns, table_data):

    app = DjangoDash('facilitiestable')

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

    return app

@register.inclusion_tag('oss/partials/facilities_table.html')
def facilities_table(site_states):
    """Produces a Dash interactive table of facilities"""

    table_columns = [dict(name='Site', id='Site', type='text', presentation='markdown'),
                     dict(name='Facility', id='Facility', type='text', presentation='markdown'),
                     dict(name='Instrument', id='Instrument', type='text', presentation='markdown'),
                     dict(name='Status', id='Status'),
                     dict(name='Comment', id='Comment')]

    table_data = []
    for site_name, site_id, site_status in site_states:
        for tel_status in site_status:
            for instrument in tel_status.instruments:
                table_data.append( dict(Site=format_link_entry(site_name, '/site/'+str(site_id)+'/'),
                                     Facility=format_link_entry(tel_status.name, '/telescope/'+str(tel_status.telescope.pk)+'/'),
                                     Instrument=format_link_entry(instrument[0], '/instrument/'+str(instrument[3])+'/'),
                                     Status=tel_status.status, #-> instrument[1],
                                     Comment=instrument[2]) )

    app = build_facilities_datatable(table_columns, table_data)

    return {'request': app}

@register.inclusion_tag('oss/partials/facilities_table.html')
def telescopes_table(tel_states):
    """Produces a Dash interactive table of facilities"""

    table_columns = [dict(name='Facility', id='Facility', type='text', presentation='markdown'),
                     dict(name='Instrument', id='Instrument', type='text', presentation='markdown'),
                     dict(name='Status', id='Status'),
                     dict(name='Comment', id='Comment')]

    table_data = []
    for tel_status in tel_states:
        for instrument in tel_status.instruments:
            table_data.append( dict(Facility=format_link_entry(tel_status.name, '/telescope/'+str(tel_status.telescope.pk)+'/'),
                                 Instrument=format_link_entry(instrument[0], '/instrument/'+str(instrument[3])+'/'),
                                 Status=tel_status.status, #-> instrument[1],
                                 Comment=instrument[2]) )

    app = build_facilities_datatable(table_columns, table_data)

    return {'request': app}
