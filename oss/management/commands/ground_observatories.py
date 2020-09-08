import json
from lco import parse_coord

def fetch_observatory_sites():
    """Function to return the geographical location of all Las Cumbres Observatory
    Network sites"""

    sites = [
        { 'name': 'Siding Spring Observatory',
          'location': 'Ground-based',
          'latitude': '31:16:23.88S',
          'longitude': '149:04:15.6E',
          'altitude': 1116.0,
          'site_code': 'coj',
          'url': 'https://www.anu.edu.au/about/campuses-facilities/siding-spring-observatory'
        },
        { 'name': 'South Africa Astronomical Observatory',
          'location': 'Ground-based',
          'latitude': '32:22:48S',
          'longitude': '20:48:36E',
          'altitude': 1460.0,
          'site_code': 'cpt',
          'url': 'https://www.saao.ac.za/'
        },
        { 'name': 'Cerro Tololo Interamerican Observatory',
          'location': 'Ground-based',
          'latitude': '30:10:2.64S',
          'longitude': '70:48:17.28W',
          'altitude': 2198.0,
          'site_code': 'lsc',
          'url': 'http://www.ctio.noao.edu/noao/'
        },
        { 'name': 'Teide Observatory',
          'location': 'Ground-based',
          'latitude': '28:18:00N',
          'longitude': '16:30:35W',
          'altitude': 2330.0,
          'site_code': 'tfn',
          'url': 'https://www.iac.es/en/observatorios-de-canarias/teide-observatory'
        },
        { 'name': 'McDonald Observatory',
          'location': 'Ground-based',
          'latitude': '30:40:12N',
          'longitude': '104:01:12W',
          'altitude': 2070.0,
          'site_code': 'elp',
          'url': 'https://mcdonaldobservatory.org/'
        },
        { 'name': 'Haleakala Observatory',
          'location': 'Ground-based',
          'latitude': '20:42:27N',
          'longitude': '156:15:21.6W',
          'altitude': 3055.0,
          'site_code': 'ogg',
          'url': 'https://www.ifa.hawaii.edu/haleakalanew/observatories.shtml'
        },
        { 'name': 'Wise Observatory',
          'location': 'Ground-based',
          'latitude': '30:35:45N',
          'longitude': '34:45:48E',
          'altitude': 875.0,
          'site_code': 'tlv',
          'url': 'http://wise-obs.tau.ac.il/general.html'
        },
        { 'name': 'Ali Observatory',
          'location': 'Ground-based',
          'latitude': '32:19:00N',
          'longitude': '80:01:00E',
          'altitude': 5100.0,
          'site_code': 'ngq',
          'url': ''
        },
        { 'name': 'Llano de Chajnantor Observatory',
          'location': 'Ground-based',
          'latitude': '23:01:22S',
          'longitude': '67:45:18W',
          'altitude': 4800.0,
          'site_code': 'ldco',
          'url': 'https://en.wikipedia.org/wiki/Llano_de_Chajnantor_Observatory'
        },
        { 'name': 'Mediterranean Sea',
          'location': 'Ground-based',
          'latitude': '42:48:00N',
          'longitude': '06:10:00E',
          'altitude': -2500.0,
          'site_code': 'medsea',
          'url': None,
        },
        { 'name': 'Apache Point',
          'location': 'Ground-based',
          'latitude': '32:46:49N',
          'longitude': '105:49:13W',
          'altitude': 2788.0,
          'site_code': 'apo',
          'url': 'https://www.apo.nmsu.edu/',
        },
        { 'name': 'Kitt Peak',
          'location': 'Ground-based',
          'latitude': '31:57:35.6N',
          'longitude': '111:35:58.92W',
          'altitude': 2133.0,
          'site_code': 'kitt',
          'url': 'https://www.noao.edu/kpno/observer_info.shtml',
        },
        { 'name': 'Mt. Graham',
          'location': 'Ground-based',
          'latitude': '32:43:08.04N',
          'longitude': '109:43:33.6W',
          'altitude': 3300.0,
          'site_code': 'mgio',
          'url': 'https://mgio.arizona.edu/',
        },
        { 'name': 'Paul Wild Observatory',
          'location': 'Ground-based',
          'latitude': '30:18:50.04S',
          'longitude': '149:33:52.56E',
          'altitude': 240.0,
          'site_code': 'pwo',
          'url': None,
        },
        { 'name': 'Mauna Loa',
          'location': 'Ground-based',
          'latitude': '19:32:11.04N',
          'longitude': '155:34:35.4W',
          'altitude': 3394.0,
          'site_code': 'mloa',
          'url': None,
        },

        ]

        for site in sites:
            site['latitude'] = parse_coord(site['latitude'])
            site['longitude'] = parse_coord(site['longitude'])

        return sites

def fetch_installations():
    """Function to return a list of dictionaries of the installations at
    different astronomical observatories around the world"""

    installations = []

    # Siding Spring, Australia
    installations.append({'name': 'AAT Dome', 'type': 'Dome', 'site_code': 'coj'})

    # Llano de Chajnantor, Atacama, Chile
    installations.append({'name': 'ALMA', 'type': 'Array', 'site_code': 'ldco'})
    installations.append({'name': 'APEX', 'type': 'Array', 'site_code': 'ldco'})

    # ANTARES, Mediterranean Sea
    installations.append({'name': 'ANTARES', 'type': 'Array', 'site_code': 'medsea'})

    # Apache Point, NM
    installations.append({'name': 'ARC 3.5m Dome', 'type': 'Dome', 'site_code': 'apo'})
    installations.append({'name': 'SDSS Dome', 'type': 'Dome', 'site_code': 'apo'})
    installations.append({'name': 'NMSU Dome', 'type': 'Dome', 'site_code': 'apo'})
    installations.append({'name': 'ARCSAT Dome', 'type': 'Dome', 'site_code': 'apo'})

    # Kitt Peak
    installations.append({'name': 'ARO 12m Dish', 'type': 'Dish', 'site_code': 'kitt'})

    # Mt. Graham
    installations.append({'name': 'Submillimeter Dish', 'type': 'Dish', 'site_code': 'mgio'})

    # Paul Wild observatory
    installations.append({'name': 'Australia Telescope Compact Array', 'type': 'Array', 'site_code': 'pwo'})

    # Mauna Loa
    installations.append({'name': 'ATLAS-MLO', 'type': 'Dome', 'site_code': 'mloa'})

    # Haleakala
    installations.append({'name': 'ATLAS-HKO', 'type': 'Dome', 'site_code': 'ogg'})
    
    return installations

def fetch_telescopes():
    """Function to return a list of dictionaries describing telescope facilities
    around the world"""

    telescopes = [
            # Siding Spring, Australia
            {'name': 'Anglo-Australian Telescope',
            'aperture': 4.0,
            'site_code': 'coj',
            'installation': 'AAT Dome',
            'tel_code': 'coj.aat.4m0a',
            'url': 'https://www.aao.gov.au/about-us/AAT',
            'operator': None},

            # Llano de Chajnantor, Atacama, Chile
            {'name': 'Atacama Large Millimeter Array',
            'aperture': 12.0,
            'site_code': 'ldco',
            'installation': 'ALMA',
            'tel_code': 'ldco.alma.12m0a',
            'url': 'https://www.almaobservatory.org/en/home/',
            'operator': None},
            {'name': 'Atacama Pathfinder Experiment',
            'aperture': 12.0,
            'site_code': 'ldco',
            'installation': 'APEX',
            'tel_code': 'ldco.apex.12m0a',
            'url': 'https://www.eso.org/public/usa/teles-instr/apex/',
            'operator': None},

            # ANTARES, Mediterranean Sea
            {'name': 'ANTARES',
            'aperture': None,
            'site_code': 'medsea',
            'installation': 'ANTARES',
            'tel_code': 'medsea.antares',
            'url': 'https://antares.in2p3.fr/',
            'operator': None},

            # Apache Point, NM
            {'name': 'Astrophysical Research Consortium 3.5m',
            'aperture': 3.5,
            'site_code': 'apo',
            'installation': 'ARC 3.5m Dome',
            'tel_code': 'apo.arc35.3m5a',
            'url': 'https://www.apo.nmsu.edu/arc35m/',
            'operator': None},

            # Kitt Peak
            {'name': 'Arizona Radio Observatory 12m',
            'aperture': 12.0,
            'site_code': 'kitt',
            'installation': 'ARO 12m Dish',
            'tel_code': 'kitt.aro.12m0a',
            'url': 'https://www.as.arizona.edu/arizona-radio-observatory',
            'operator': None},

            # Mt. Graham
            {'name': 'Submillimeter Telescope',
            'aperture': None,
            'site_code': 'mgio',
            'installation': 'Submillimeter Dish',
            'tel_code': 'mgio.smt',
            'url': 'https://www.as.arizona.edu/arizona-radio-observatory',
            'operator': None},

            # Paul Wild Observatory, Australia
            {'name': 'Australia Telescope Compact Array',
            'aperture': 22.0,
            'site_code': 'pwo',
            'installation': 'Australia Telescope Compact Array',
            'tel_code': 'pwo.atca',
            'url': 'https://www.narrabri.atnf.csiro.au/',
            'operator': None},

            # Hawai'i
            {'name': 'ATLAS-MLO',
            'aperture': 0.5,
            'site_code': 'mloa',
            'installation': 'ATLAS-MLO',
            'tel_code': 'mloa.atlas-mlo.0m5a',
            'url': 'https://atlas.fallingstar.com/home.php',
            'operator': None},
            {'name': 'ATLAS-HKO',
            'aperture': 0.5,
            'site_code': 'ogg',
            'installation': 'ATLAS-HKO',
            'tel_code': 'ogg.atlas-hko.0m5a',
            'url': 'https://atlas.fallingstar.com/home.php',
            'operator': None},
            ]

    return telescopes

def fetch_instruments():
    """Function to return a list of dictionaries describing instruments"""

    instruments = [
        # Siding Spring, Australia
        {'name': 'AAOmega',
        'site_code': 'coj',
        'tel_code': 'coj.aat.4m0a',
        'installation': 'AAT Dome',
        'telescope': 'Anglo-Australian Telescope',
        'wavelength': 'Optical',
        'capabilities': ['Wide-field fibre-fed spectroscopy'],
        'url': 'https://aat.anu.edu.au/science/instruments/current/AAOmega'},
        {'name': 'HERMES',
        'site_code': 'coj',
        'tel_code': 'coj.aat.4m0a',
        'installation': 'AAT Dome',
        'telescope': 'Anglo-Australian Telescope',
        'wavelength': 'Optical',
        'capabilities': ['High-resolution spectroscopy'],
        'url': 'https://aat.anu.edu.au/science/instruments/current/HERMES'},
        {'name': 'Veloce',
        'site_code': 'coj',
        'tel_code': 'coj.aat.4m0a',
        'installation': 'AAT Dome',
        'telescope': 'Anglo-Australian Telescope',
        'wavelength': 'Optical',
        'capabilities': ['Echelle spectroscopy'],
        'url': 'https://aat.anu.edu.au/science/instruments/current/veloce/overview'},

        # ALMA
        {'name': 'Interferometer',
        'site_code': 'ldco',
        'tel_code': 'ldco.alma.12m0a',
        'installation': 'ALMA',
        'telescope': 'ALMA',
        'wavelength': 'Millimeter',
        'capabilities': ['Interferometry'],
        'url': 'https://almascience.nrao.edu/proposing/proposers-guide'},
        {'name': 'LABOCA',
        'site_code': 'ldco',
        'tel_code': 'ldco.apex.12m0a',
        'installation': 'APEX',
        'telescope': 'APEX',
        'wavelength': 'Millimeter',
        'capabilities': ['Bolometer'],
        'url': 'https://www.eso.org/public/teles-instr/apex/laboca/'},

        # ANTARES
        {'name': 'Cherenkov array',
        'site_code': 'medsea',
        'tel_code': 'medsea.antares',
        'installation': 'ANTARES',
        'telescope': 'ANTARES',
        'wavelength': 'Neutrino',
        'capabilities': ['Neutrino detection'],
        'url': 'https://antares.in2p3.fr/'},

        # Apache Point, NM
        {'name': 'ARCES',
        'site_code': 'apo',
        'tel_code': 'apo.arc35m.3m5a',
        'installation': 'ARC 3.5m Dome',
        'telescope': 'Astrophysical Research Consortium 3.5m',
        'wavelength': 'Optical',
        'capabilities': ['Echelle spectroscopy'],
        'url': 'https://www.apo.nmsu.edu/arc35m/Instruments/ARCES/'},
        {'name': 'DIS',
        'site_code': 'apo',
        'tel_code': 'apo.arc35m.3m5a',
        'installation': 'ARC 3.5m Dome',
        'telescope': 'Astrophysical Research Consortium 3.5m',
        'wavelength': 'Optical',
        'capabilities': ['Long-slit spectroscopy'],
        'url': 'https://www.apo.nmsu.edu/arc35m/Instruments/DIS/'},
        {'name': 'NIC-FPS',
        'site_code': 'apo',
        'tel_code': 'apo.arc35m.3m5a',
        'installation': 'ARC 3.5m Dome',
        'telescope': 'Astrophysical Research Consortium 3.5m',
        'wavelength': 'Infrared',
        'capabilities': ['Imaging', 'Fabry-Perot spectrometer'],
        'url': 'https://www.apo.nmsu.edu/arc35m/Instruments/NICFPS/'},
        {'name': 'AGILE',
        'site_code': 'apo',
        'tel_code': 'apo.arc35m.3m5a',
        'installation': 'ARC 3.5m Dome',
        'telescope': 'Astrophysical Research Consortium 3.5m',
        'wavelength': 'Optical',
        'capabilities': ['Photometer'],
        'url': 'https://www.apo.nmsu.edu/arc35m/Instruments/AGILE/'},
        {'name': 'ARCTIC',
        'site_code': 'apo',
        'tel_code': 'apo.arc35m.3m5a',
        'installation': 'ARC 3.5m Dome',
        'telescope': 'Astrophysical Research Consortium 3.5m',
        'wavelength': 'Optical',
        'capabilities': ['Imaging'],
        'url': 'https://www.apo.nmsu.edu/arc35m/Instruments/ARCTIC/'},
        {'name': 'TRIPLESPEC',
        'site_code': 'apo',
        'tel_code': 'apo.arc35m.3m5a',
        'installation': 'ARC 3.5m Dome',
        'telescope': 'Astrophysical Research Consortium 3.5m',
        'wavelength': 'Infrared',
        'capabilities': ['Long-slit spectroscopy'],
        'url': 'https://www.apo.nmsu.edu/arc35m/Instruments/TRIPLESPEC/'},

        # ATLAS
        {'name': 'ATLAS Imager',
        'site_code': 'mloa',
        'tel_code': 'mloa.atlas-mlo.0m5a',
        'installation': 'ATLAS-MLO',
        'telescope': 'ATLAS-MLO',
        'wavelength': 'Optical',
        'capabilities': ['Imaging'],
        'url': 'https://atlas.fallingstar.com/how_atlas_works.php'},
        {'name': 'ATLAS Imager',
        'site_code': 'ogg',
        'tel_code': 'ogg.atlas-hko.0m5a',
        'installation': 'ATLAS-HKO',
        'telescope': 'ATLAS-HKO',
        'wavelength': 'Optical',
        'capabilities': ['Imaging'],
        'url': 'https://atlas.fallingstar.com/how_atlas_works.php'},

        ]

    return instruments
