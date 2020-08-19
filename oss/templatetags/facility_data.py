from django import template
from django.conf import settings

register = template.Library()

@register.inclusion_tag('oss/partials/facility_list_entry.html')
def telescope_status_entry(tel_status):
    """
    Formats the display of the facility's status information
    """

    status_map = {'Closed-weather': {'bgcolor': '#0349fc', 'fontcolor': '#ffffff'},
                  'Open': {'bgcolor': '#00d620', 'fontcolor': '#ffffff'},
                  'Offline': {'bgcolor': '#d65900', 'fontcolor': '#ffffff'},
                  'Unknown': {'bgcolor': '#ffffff', 'fontcolor': '#000000'}}

    tel_bgcolor = status_map[tel_status.status]['bgcolor']
    tel_fontcolor = status_map[tel_status.status]['fontcolor']

    bgcolors = []
    fontcolors = []

    instruments = []
    for instrument in tel_status.instruments:
        bg = status_map[instrument[1]]['bgcolor']
        font = status_map[instrument[1]]['fontcolor']
        instruments.append( list(instruments) + [bg, font] )

    return {'tel_status': tel_status,
            'tel_bgcolor': tel_bgcolor, 'tel_fontcolor': tel_fontcolor,
            'instruments': instruments}
