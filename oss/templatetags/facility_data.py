from django import template
from django.conf import settings

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
