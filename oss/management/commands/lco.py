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
          'site_code': 'coj'
        },
        { 'name': 'South Africa Astronomical Observatory',
          'location': 'Ground-based',
          'latitude': '32:22:48S',
          'longitude': '20:48:36E',
          'altitude': 1460.0,
          'site_code': 'cpt'
        },
        { 'name': 'Cerro Tololo Interamerican Observatory',
          'location': 'Ground-based',
          'latitude': '30:10:2.64S',
          'longitude': '70:48:17.28W',
          'altitude': 2198.0,
          'site_code': 'lsc'
        },
        { 'name': 'Teide Observatory',
          'location': 'Ground-based',
          'latitude': '28:18:00N',
          'longitude': '16:30:35W',
          'altitude': 2330.0,
          'site_code': 'tfn'
        },
        { 'name': 'McDonald Observatory',
          'location': 'Ground-based',
          'latitude': '30:40:12N',
          'longitude': '104:01:12W',
          'altitude': 2070.0,
          'site_code': 'elp'
        },
        { 'name': 'Haleakala Observatory',
          'location': 'Ground-based',
          'latitude': '20:42:27N',
          'longitude': '156:15:21.6W',
          'altitude': 3055.0,
          'site_code': 'ogg'
        },
        { 'name': 'Wise Observatory',
          'location': 'Ground-based',
          'latitude': '30:35:45N',
          'longitude': '34:45:48E',
          'altitude': 875.0,
          'site_code': 'tlv'
        },
        { 'name': 'Ali Observatory',
          'location': 'Ground-based',
          'latitude': '32:19:00N',
          'longitude': '80:01:00E',
          'altitude': 5100.0,
          'site_code': 'ngq'
        }
    ]

    for site in sites:
        site['latitude'] = parse_coord(site['latitude'])
        site['longitude'] = parse_coord(site['longitude'])

    return sites

def fetch_lco_installations():
    """Function to return the details of all LCO site installations,
    which in this case means enclosures/domes"""

    installations = []
    # Australia
    installations.append({'name': 'LCO Clamshell', 'type': 'Dome', 'site_code': 'coj'})
    for dome in ['LCO Dome A', 'LCO Dome B', 'LCO Dome C']:
        installations.append({'name': dome, 'type': 'Dome', 'site_code': 'coj'})

    # Israel
    installations.append({'name': 'LCO Dome A', 'type': 'Dome', 'site_code': 'tlv'})

    # South Africa
    for dome in ['LCO Dome A', 'LCO Dome B', 'LCO Dome C']:
        installations.append({'name': dome, 'type': 'Dome', 'site_code': 'cpt'})
    installations.append({'name': 'LCO Aqawan A', 'type': 'Dome', 'site_code': 'cpt'})

    # Tenerife
    installations.append({'name': 'LCO Aqawan A', 'type': 'Dome', 'site_code': 'tfn'})

    # Chile
    for dome in ['LCO Dome A', 'LCO Dome B', 'LCO Dome C', 'LCO Aqawan A', 'LCO Aqawan B']:
        installations.append({'name': dome, 'type': 'Dome', 'site_code': 'lsc'})

    # Texas
    for dome in ['LCO Dome A', 'LCO Dome B', 'LCO Dome C', 'LCO Aqawan A']:
        installations.append({'name': dome, 'type': 'Dome', 'site_code': 'elp'})

    # Hawai'i
    installations.append({'name': 'LCO Clamshell', 'type': 'Dome', 'site_code': 'ogg'})
    for dome in ['LCO Dome A', 'LCO Dome B', 'LCO Dome C']:
        installations.append({'name': dome, 'type': 'Dome', 'site_code': 'ogg'})

    return installations

def fetch_lco_telescopes():
    """
    Function to return the details of all LCO telescopes
    """

    telescopes = [
            # LCO Australia
            {'name': 'Faulkes Telescope South',
            'aperture': 2.0,
            'site_code': 'coj',
            'installation': 'LCO Clamshell',
            'tel_code': 'coj.clma.2m0a'
            },
            {'name': '1m0a',
            'aperture': 1.0,
            'site_code': 'coj',
            'installation': 'LCO Dome A',
            'tel_code': 'coj.doma.1m0a'
            },
            {'name': '1m0a',
            'aperture': 1.0,
            'site_code': 'coj',
            'installation': 'LCO Dome B',
            'tel_code': 'coj.domb.1m0a'
            },
            {'name': '1m0a',
            'aperture': 1.0,
            'site_code': 'coj',
            'installation': 'LCO Dome C',
            'tel_code': 'coj.domc.1m0a'
            },
            {'name': '0m4a',
            'aperture': 0.4,
            'site_code': 'coj',
            'installation': 'LCO Clamshell',
            'tel_code': 'coj.clma.0m4a'
            },
            {'name': '0m4b',
            'aperture': 0.4,
            'site_code': 'coj',
            'installation': 'LCO Clamshell',
            'tel_code': 'coj.clma.0m4b'
            },

            # LCO Israel
            {'name': '1m0a',
            'aperture': 1.0,
            'site_code': 'tlv',
            'installation': 'LCO Dome A',
            'tel_code': 'tlv.doma.1m0a'
            },

            # LCO South Africa
            {'name': '1m0a',
            'aperture': 1.0,
            'site_code': 'cpt',
            'installation': 'LCO Dome A',
            'tel_code': 'cpt.doma.1m0a'
            },
            {'name': '1m0a',
            'aperture': 1.0,
            'site_code': 'cpt',
            'installation': 'LCO Dome B',
            'tel_code': 'cpt.domb.1m0a'
            },
            {'name': '1m0a',
            'aperture': 1.0,
            'site_code': 'cpt',
            'installation': 'LCO Dome C',
            'tel_code': 'cpt.domc.1m0a'
            },
            {'name': '0m4a',
            'aperture': 0.4,
            'site_code': 'cpt',
            'installation': 'LCO Aqawan A',
            'tel_code': 'cpt.aqwa.0m4a'
            },


            # LCO Tenerife
            {'name': '0m4a',
            'aperture': 0.4,
            'site_code': 'tfn',
            'installation': 'LCO Aqawan A',
            'tel_code': 'tfn.aqwa.0m4a'
            },
            {'name': '0m4b',
            'aperture': 0.4,
            'site_code': 'tfn',
            'installation': 'LCO Aqawan A',
            'tel_code': 'tfn.aqwa.0m4b'
            },

            # LCO Chile
            {'name': '1m0a',
            'aperture': 1.0,
            'site_code': 'lsc',
            'installation': 'LCO Dome A',
            'tel_code': 'lsc.doma.1m0a'
            },
            {'name': '1m0a',
            'aperture': 1.0,
            'site_code': 'lsc',
            'installation': 'LCO Dome B',
            'tel_code': 'lsc.domb.1m0a'
            },
            {'name': '1m0a',
            'aperture': 1.0,
            'site_code': 'lsc',
            'installation': 'LCO Dome C',
            'tel_code': 'lsc.domc.1m0a'
            },
            {'name': '0m4a',
            'aperture': 0.4,
            'site_code': 'lsc',
            'installation': 'LCO Aqawan A',
            'tel_code': 'lsc.aqwa.0m4a'
            },
            {'name': '0m4a',
            'aperture': 0.4,
            'site_code': 'lsc',
            'installation': 'LCO Aqawan B',
            'tel_code': 'lsc.aqwb.0m4a'
            },

            # LCO Texas
            {'name': '1m0a',
            'aperture': 1.0,
            'site_code': 'elp',
            'installation': 'LCO Dome A',
            'tel_code': 'elp.doma.1m0a'
            },
            {'name': '1m0a',
            'aperture': 1.0,
            'site_code': 'elp',
            'installation': 'LCO Dome B',
            'tel_code': 'elp.domb.1m0a'
            },
            {'name': '0m4a',
            'aperture': 0.4,
            'site_code': 'elp',
            'installation': 'LCO Aqawan A',
            'tel_code': 'elp.aqwa.0m4a'
            },

            # LCO Hawai'i
            {'name': 'Faulkes Telescope North',
            'aperture': 2.0,
            'site_code': 'ogg',
            'installation': 'LCO Clamshell',
            'tel_code': 'ogg.clma.2m0a'
            },
            {'name': '0m4a',
            'aperture': 0.4,
            'site_code': 'ogg',
            'installation': 'LCO Clamshell',
            'tel_code': 'ogg.clma.0m4a'
            },
            {'name': '0m4b',
            'aperture': 0.4,
            'site_code': 'ogg',
            'installation': 'LCO Clamshell',
            'tel_code': 'ogg.clma.0m4b'
            },
            {'name': '0m4c',
            'aperture': 0.4,
            'site_code': 'ogg',
            'installation': 'LCO Clamshell',
            'tel_code': 'ogg.clma.0m4c'
            }
    ]

    for tel in telescopes:
        tel['operator'] = 'Las Cumbres Observatory'

    return telescopes

def fetch_lco_instruments():
    """Function to return the details of all LCO instruments"""

    instruments = [
        # LCO Australia
        {'name': 'fs01 Spectral',
        'site_code': 'coj',
        'tel_code': 'coj.clma.2m0a',
        'installation': 'LCO Clamshell',
        'telescope': 'Faulkes Telescope South',
        'wavelength': 'Optical',
        'capabilities': ['Imaging']},
        {'name': 'en12 FLOYDS',
        'site_code': 'coj',
        'tel_code': 'coj.clma.2m0a',
        'installation': 'LCO Clamshell',
        'telescope': 'Faulkes Telescope South',
        'wavelength': 'Optical',
        'capabilities': ['Long-slit spectroscopy']},
        {'name': 'kb28 SBIG',
        'site_code': 'coj',
        'tel_code': 'coj.clma.0m4a',
        'installation': 'LCO Clamshell',
        'telescope': '0m4a',
        'wavelength': 'Optical',
        'capabilities': ['Imaging']},
        {'name': 'kb56 SBIG',
        'site_code': 'coj',
        'tel_code': 'coj.clma.0m4b',
        'installation': 'LCO Clamshell',
        'telescope': '0m4b',
        'wavelength': 'Optical',
        'capabilities': ['Imaging']},
        {'name': 'fa12 Sinistro',
        'site_code': 'coj',
        'tel_code': 'coj.doma.1m0a',
        'installation': 'LCO Dome A',
        'telescope': '1m0a',
        'wavelength': 'Optical',
        'capabilities': ['Imaging']},
        {'name': 'fa19 Sinistro',
        'site_code': 'coj',
        'tel_code': 'coj.domb.1m0a',
        'installation': 'LCO Dome B',
        'telescope': '1m0a',
        'wavelength': 'Optical',
        'capabilities': ['Imaging']},

        # LCO Israel
        {'name': 'NRES-agu-ak13',
        'site_code': 'tlv',
        'tel_code': 'tlv.doma.1m0a',
        'installation': 'LCO Dome A',
        'telescope': '1m0a',
        'wavelength': 'Optical',
        'capabilities': ['Echelle spectroscopy']},

        # LCO South Africa
        {'name': 'fa16 Sinistro',
        'site_code': 'cpt',
        'tel_code': 'cpt.doma.1m0a',
        'installation': 'LCO Dome A',
        'telescope': '1m0a',
        'wavelength': 'Optical',
        'capabilities': ['Imaging']},
        {'name': 'fa14 Sinistro',
        'site_code': 'cpt',
        'tel_code': 'cpt.domb.1m0a',
        'installation': 'LCO Dome B',
        'telescope': '1m0a',
        'wavelength': 'Optical',
        'capabilities': ['Imaging']},
        {'name': 'NRES',
        'site_code': 'cpt',
        'tel_code': 'cpt.domb.1m0a',
        'installation': 'LCO Dome B',
        'telescope': '1m0a',
        'wavelength': 'Optical',
        'capabilities': ['Echelle spectroscopy']},
        {'name': 'fa06 Sinistro',
        'site_code': 'cpt',
        'tel_code': 'cpt.domc.1m0a',
        'installation': 'LCO Dome C',
        'telescope': '1m0a',
        'wavelength': 'Optical',
        'capabilities': ['Imaging']},
        {'name': 'kb84 SBIG',
        'site_code': 'cpt',
        'tel_code': 'cpt.aqwa.0m4a',
        'installation': 'LCO Aqawan A',
        'telescope': '0m4a',
        'wavelength': 'Optical',
        'capabilities': ['Imaging']},

        # LCO Tenerife
        {'name': 'kb81 SBIG',
        'site_code': 'tfn',
        'tel_code': 'tfn.aqwa.0m4a',
        'installation': 'LCO Aqawan A',
        'telescope': '0m4a',
        'wavelength': 'Optical',
        'capabilities': ['Imaging']},
        {'name': 'kb98 SBIG',
        'site_code': 'tfn',
        'tel_code': 'tfn.aqwa.0m4b',
        'installation': 'LCO Aqawan A',
        'telescope': '0m4b',
        'wavelength': 'Optical',
        'capabilities': ['Imaging']},

        # LCO Chile
        {'name': 'fa15 Sinistro',
        'site_code': 'lsc',
        'tel_code': 'lsc.doma.1m0a',
        'installation': 'LCO Dome A',
        'telescope': '1m0a',
        'wavelength': 'Optical',
        'capabilities': ['Imaging']},
        {'name': 'fa04 Sinistro',
        'site_code': 'lsc',
        'tel_code': 'lsc.domb.1m0a',
        'installation': 'LCO Dome B',
        'telescope': '1m0a',
        'wavelength': 'Optical',
        'capabilities': ['Imaging']},
        {'name': 'NRES',
        'site_code': 'lsc',
        'tel_code': 'lsc.domb.1m0a',
        'installation': 'LCO Dome B',
        'telescope': '1m0a',
        'wavelength': 'Optical',
        'capabilities': ['Echelle spectroscopy']},
        {'name': 'fa03 Sinistro',
        'site_code': 'lsc',
        'tel_code': 'lsc.domc.1m0a',
        'installation': 'LCO Dome C',
        'telescope': '1m0a',
        'wavelength': 'Optical',
        'capabilities': ['Imaging']},
        {'name': 'kb29 SBIG',
        'site_code': 'lsc',
        'tel_code': 'lsc.aqwa.0m4a',
        'installation': 'LCO Aqawan A',
        'telescope': '0m4a',
        'wavelength': 'Optical',
        'capabilities': ['Imaging']},
        {'name': 'kb26 SBIG',
        'site_code': 'lsc',
        'tel_code': 'lsc.aqwb.0m4a',
        'installation': 'LCO Aqawan B',
        'telescope': '0m4a',
        'wavelength': 'Optical',
        'capabilities': ['Imaging']},

        # LCO Texas
        {'name': 'fa05 Sinistro',
        'site_code': 'elp',
        'tel_code': 'elp.doma.1m0a',
        'installation': 'LCO Dome A',
        'telescope': '1m0a',
        'wavelength': 'Optical',
        'capabilities': ['Imaging']},
        {'name': 'fa07 Sinistro',
        'site_code': 'elp',
        'tel_code': 'elp.domb.1m0a',
        'installation': 'LCO Dome B',
        'telescope': '1m0a',
        'wavelength': 'Optical',
        'capabilities': ['Imaging']},
        {'name': 'kb92 SBIG',
        'site_code': 'elp',
        'tel_code': 'elp.aqwa.0m4a',
        'installation': 'LCO Aqawan A',
        'telescope': '0m4a',
        'wavelength': 'Optical',
        'capabilities': ['Imaging']},

        # LCO Hawai'i
        {'name': 'fs02 Spectral',
        'site_code': 'ogg',
        'tel_code': 'ogg.clma.2m0a',
        'installation': 'LCO Clamshell',
        'telescope': 'Faulkes Telescope North',
        'wavelength': 'Optical',
        'capabilities': ['Imaging']},
        {'name': 'en06 FLOYDS',
        'site_code': 'ogg',
        'tel_code': 'ogg.clma.2m0a',
        'installation': 'LCO Clamshell',
        'telescope': 'Faulkes Telescope North',
        'wavelength': 'Optical',
        'capabilities': ['Long-slit spectroscopy']},
        {'name': 'kb27 SBIG',
        'site_code': 'ogg',
        'tel_code': 'ogg.clma.0m4b',
        'installation': 'LCO Clamshell',
        'telescope': '0m4b',
        'wavelength': 'Optical',
        'capabilities': ['Imaging']},
        {'name': 'kb82 SBIG',
        'site_code': 'ogg',
        'tel_code': 'ogg.clma.0m4c',
        'installation': 'LCO Clamshell',
        'telescope': '0m4c',
        'wavelength': 'Optical',
        'capabilities': ['Imaging']},
        ]

    return instruments

def get_lco_tel_codes():

    lco_instruments = fetch_lco_instruments()
    lco_tel_codes = []
    for instrument in lco_instruments:
        lco_tel_codes.append(instrument['tel_code'])

    return lco_tel_codes

def fetch_lco_telescope_states():
    """Function to query the Las Cumbres Observatory API for a readout of
    the current states of its telescopes"""

    url = path.join(API_ROOT, 'telescope_states')
    response = requests.get(url).json()

    return response

def fetch_lco_telescope_availability():
    """Function to query the Las Cumbres Observatory API for a readout of
    the current availability of its telescopes"""

    url = path.join(API_ROOT, 'telescope_availability')
    response = requests.get(url).json()

    return response

if __name__ == '__main__':
    fetch_lco_telescope_states()
