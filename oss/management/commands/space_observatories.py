import json
from lco import parse_coord

def fetch_space_sites():
    """Function to return a list of dictionaries describing the orbital
    locations of space-based facilities.  Site is a misnomer here, used
    simply to give parity with the ground-based facilities."""

    sites = [
        { 'name': 'Equatorial orbit',
          'location': 'Space',
          'orbit': 'Equatorial Earth orbit',
          'site_code': 'orb-earth-equ',
          'url': None,
        },
        { 'name': 'Earth orbit',
          'location': 'Space',
          'orbit': 'Earth orbit',
          'site_code': 'orb-earth',
          'url': None,
        },
        ]

    return sites

def fetch_space_installations():
    """Function to return a list of dictionaries describing space-based
    installations"""

    installations = []
    installations.append({'name': 'AGILE', 'type': 'Spacecraft', 'site_code': 'orb-earth-equ'})
    installations.append({'name': 'Chandra', 'type': 'Spacecraft', 'site_code': 'orb-earth'})
    installations.append({'name': 'Fermi', 'type': 'Spacecraft', 'site_code': 'orb-earth'})

    return installations

def fetch_space_telescopes():
    """Function to return a list of dictionaries describing space-based
    telescope facilities"""

    telescopes = [
            {'name': 'AGILE',
            'aperture': None,
            'site_code': 'orb-earth-equ',
            'installation': 'AGILE',
            'tel_code': 'orb-earth-equ.agile',
            'url': 'http://agile.rm.iasf.cnr.it/',
            'operator': None},
            {'name': 'Chandra',
            'aperture': None,
            'site_code': 'orb-earth',
            'installation': 'Chandra',
            'tel_code': 'orb-earth.chandra',
            'url': 'https://chandra.harvard.edu/index.html',
            'operator': None},
            {'name': 'Fermi',
            'aperture': None,
            'site_code': 'orb-earth',
            'installation': 'Fermi',
            'tel_code': 'orb-earth.fermi',
            'url': 'https://fermi.gsfc.nasa.gov/'',
            'operator': None},
                ]

    return telescopes

def fetch_space_instruments():
    """Function to return a list of dictionaries describing instruments"""

    instruments = [
            # AGILE
            {'name': 'Gamma Ray Imaging Detector',
            'site_code': 'orb-earth-equ',
            'tel_code': 'orb-earth-equ.agile',
            'installation': 'AGILE',
            'telescope': 'AGILE',
            'wavelength': 'Gamma ray',
            'capabilities': ['Imaging'],
            'url': None},
            {'name': 'SuperAGILE',
            'site_code': 'orb-earth-equ',
            'tel_code': 'orb-earth-equ.agile',
            'installation': 'AGILE',
            'telescope': 'AGILE',
            'wavelength': 'X-ray',
            'capabilities': ['Imaging'],
            'url': None},
            {'name': 'Mini-Calorimeter',
            'site_code': 'orb-earth-equ',
            'tel_code': 'orb-earth-equ.agile',
            'installation': 'AGILE',
            'telescope': 'AGILE',
            'wavelength': 'Gamma ray',
            'capabilities': ['Scintillation detector'],
            'url': None},
            {'name': 'High Resolution Camera',
            'site_code': 'orb-earth',
            'tel_code': 'orb-earth.chandra',
            'installation': 'Chandra',
            'telescope': 'Chandra',
            'wavelength': 'X-ray',
            'capabilities': ['Imaging'],
            'url': },
            {'name': 'Advanced CCD Imaging Spectrometer',
            'site_code': 'orb-earth',
            'tel_code': 'orb-earth.chandra',
            'installation': 'Chandra',
            'telescope': 'Chandra',
            'wavelength': 'X-ray',
            'capabilities': ['Imaging', 'Spectrometry'],
            'url': None},
            {'name': 'High Resolution Transmission Grating Spectrometer',
            'site_code': 'orb-earth',
            'tel_code': 'orb-earth.chandra',
            'installation': 'Chandra',
            'telescope': 'Chandra',
            'wavelength': 'X-ray',
            'capabilities': ['Spectroscopy'],
            'url': 'https://space.mit.edu/HETG/hetg_info.html'},
            {'name': 'Low Energy Transmission Grating Spectrometer',
            'site_code': 'orb-earth',
            'tel_code': 'orb-earth.chandra',
            'installation': 'Chandra',
            'telescope': 'Chandra',
            'wavelength': 'X-ray',
            'capabilities': ['Spectroscopy'],
            'url': None},
    ]

    return instruments
