import requests
import json
from os import path

API_ROOT = 'https://observe.lco.global/api/'

def parse_coord(coord_str):
    if 'S' in coord_str or 'W' in coord_str:
        sign = -1.0
    else:
        sign = 1.0
    coord_str = coord_str.replace('S','').replace('N','').replace('E','').replace('W','')

    (deg, mins, secs) = coord_str.split(':')
    coord = float(deg) + (float(mins)/60.0) + (float(secs)/3600.0)
    coord *= sign

    return coord

def parse_site_code(site_code):
    """Function to provide the mapping between the LCO site code and the long-hand
    name of the observatory as stored in the DB"""

    sites_dict = { 'coj': 'Siding Spring Observatory',
                   'cpt': 'South Africa Astronomical Observatory',
                   'lsc': 'Cerro Tololo Interamerican Observatory',
                   'tfn': 'Teide Observatory',
                   'elp': 'McDonald Observatory',
                   'ogg': 'Haleakala Observatory',
                   'tlv': 'Wise Observatory',
                   'ngq': 'Ali Observatory' }

    return sites_dict[site_code]

def parse_aperture_from_telid(tel_id):
    """Function to return the telescope aperture from the tel_id string"""

    for code in ['a', 'b', 'c', 'm']:
        tel_id = tel_id.replace(code,'')

    return float(tel_id)

def fetch_lco_sites():
    """Function to return the geographical location of all Las Cumbres Observatory
    Network sites"""

    sites = [
        { 'name': 'Siding Spring Observatory',
          'location': 'Ground-based',
          'latitude': '31:16:23.88S',
          'longitude': '149:04:15.6E',
          'altitude': 1116.0,
        },
        { 'name': 'South Africa Astronomical Observatory',
          'location': 'Ground-based',
          'latitude': '32:22:48S',
          'longitude': '20:48:36E',
          'altitude': 1460.0,
        },
        { 'name': 'Cerro Tololo Interamerican Observatory',
          'location': 'Ground-based',
          'latitude': '30:10:2.64S',
          'longitude': '70:48:17.28W',
          'altitude': 2198.0,
        },
        { 'name': 'Teide Observatory',
          'location': 'Ground-based',
          'latitude': '28:18:00N',
          'longitude': '16:30:35W',
          'altitude': 2330.0,
        },
        { 'name': 'McDonald Observatory',
          'location': 'Ground-based',
          'latitude': '30:40:12N',
          'longitude': '104:01:12W',
          'altitude': 2070.0,
        },
        { 'name': 'Haleakala Observatory',
          'location': 'Ground-based',
          'latitude': '20:42:27N',
          'longitude': '156:15:21.6W',
          'altitude': 3055.0,
        },
        { 'name': 'Wise Observatory',
          'location': 'Ground-based',
          'latitude': '30:35:45N',
          'longitude': '34:45:48E',
          'altitude': 875.0,
        },
        { 'name': 'Ali Observatory',
          'location': 'Ground-based',
          'latitude': '32:19:00N',
          'longitude': '80:01:00E',
          'altitude': 5100.0,
        }
    ]
    for site in sites:
        site['latitude'] = parse_coord(site['latitude'])
        site['longitude'] = parse_coord(site['longitude'])

    return sites

def fetch_lco_instruments():
    """Function to return the details of all LCO instruments"""

    instruments = [
        # LCO Australia
        {'name': 'fs01 Spectral',
        'site_code': 'coj.clma.2m0a',
        'wavelength': 'Optical',
        'capabilities': ['Imaging']},
        {'name': 'en12 FLOYDS',
        'site_code': 'coj.clma.2m0a',
        'wavelength': 'Optical',
        'capabilities': ['Long-slit spectroscopy']},
        {'name': 'kb28 SBIG',
        'site_code': 'coj.clma.0m4a',
        'wavelength': 'Optical',
        'capabilities': ['Imaging']},
        {'name': 'kb56 SBIG',
        'site_code': 'coj.clma.0m4b',
        'wavelength': 'Optical',
        'capabilities': ['Imaging']},
        {'name': 'fa12 Sinistro',
        'site_code': 'coj.doma.1m0a',
        'wavelength': 'Optical',
        'capabilities': ['Imaging']},
        {'name': 'fa19 Sinistro',
        'site_code': 'coj.domb.1m0a',
        'wavelength': 'Optical',
        'capabilities': ['Imaging']},

        # LCO Israel
        {'name': 'nres-agu-ak13',
        'site_code': 'tlv.doma.1m0a',
        'wavelength': 'Optical',
        'capabilities': ['Echelle spectroscopy']},

        # LCO South Africa
        {'name': 'fa16 Sinistro',
        'site_code': 'cpt.doma.1m0a',
        'wavelength': 'Optical',
        'capabilities': ['Imaging']},
        {'name': 'fa14 Sinistro',
        'site_code': 'cpt.domb.1m0a',
        'wavelength': 'Optical',
        'capabilities': ['Imaging', 'Echelle spectroscopy']},
        {'name': 'fa06 Sinistro',
        'site_code': 'cpt.domc.1m0a',
        'wavelength': 'Optical',
        'capabilities': ['Imaging']},
        {'name': 'kb84 SBIG',
        'site_code': 'cpt.aqwa.1m0a',
        'wavelength': 'Optical',
        'capabilities': ['Imaging']},

        # LCO Tenerife
        {'name': 'kb81 SBIG',
        'site_code': 'tfn.aqwa.1m0a',
        'wavelength': 'Optical',
        'capabilities': ['Imaging']},
        {'name': 'kb98 SBIG',
        'site_code': 'tfn.aqwa.1m0b',
        'wavelength': 'Optical',
        'capabilities': ['Imaging']},

        # LCO Chile
        {'name': 'fa15 Sinistro',
        'site_code': 'lsc.doma.1m0a',
        'wavelength': 'Optical',
        'capabilities': ['Imaging']},
        {'name': 'fa04 Sinistro',
        'site_code': 'lsc.domb.1m0a',
        'wavelength': 'Optical',
        'capabilities': ['Imaging', 'Echelle spectroscopy']},
        {'name': 'fa03 Sinistro',
        'site_code': 'lsc.domc.1m0a',
        'wavelength': 'Optical',
        'capabilities': ['Imaging']},
        {'name': 'kb29 SBIG',
        'site_code': 'lsc.aqwa.1m0a',
        'wavelength': 'Optical',
        'capabilities': ['Imaging']},
        {'name': 'kb26 SBIG',
        'site_code': 'lsc.aqwb.1m0a',
        'wavelength': 'Optical',
        'capabilities': ['Imaging']},

        # LCO Texas
        {'name': 'fa05 Sinistro',
        'site_code': 'elp.doma.1m0a',
        'wavelength': 'Optical',
        'capabilities': ['Imaging']},
        {'name': 'fa07 Sinistro',
        'site_code': 'elp.domb.1m0a',
        'wavelength': 'Optical',
        'capabilities': ['Imaging']},
        {'name': 'kb92 SBIG',
        'site_code': 'elp.aqwa.1m0a',
        'wavelength': 'Optical',
        'capabilities': ['Imaging']},

        # LCO Hawai'i
        {'name': 'fs02 Spectral',
        'site_code': 'ogg.clma.2m0a',
        'wavelength': 'Optical',
        'capabilities': ['Imaging']},
        {'name': 'en06 FLOYDS',
        'site_code': 'ogg.clma.2m0a',
        'wavelength': 'Optical',
        'capabilities': ['Long-slit spectroscopy']},
        {'name': 'kb27 SBIG',
        'site_code': 'ogg.clma.0m4b',
        'wavelength': 'Optical',
        'capabilities': ['Imaging']},
        {'name': 'kb82 SBIG',
        'site_code': 'ogg.clma.0m4c',
        'wavelength': 'Optical',
        'capabilities': ['Imaging']},
        ]

    return instruments
    
def fetch_lco_telescope_states():
    """Function to query the Las Cumbres Observatory API for a readout of
    the current states of its telescopes"""

    url = path.join(API_ROOT, 'telescope_states')
    response = requests.get(url).json()

    return response

if __name__ == '__main__':
    fetch_lco_telescope_states()
