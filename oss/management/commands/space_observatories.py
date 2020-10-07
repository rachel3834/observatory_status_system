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
        { 'name': 'Low Earth Orbit',
          'location': 'Space',
          'orbit': 'Low Earth Orbit',
          'site_code': 'orb-earth-low',
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
    installations.append({'name': 'HST', 'type': 'Spacecraft', 'site_code': 'orb-earth-low'})
    installations.append({'name': 'INTEGRAL', 'type': 'Spacecraft', 'site_code': 'orb-earth'})

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
            'url': 'https://fermi.gsfc.nasa.gov/',
            'operator': None},
            {'name': 'Hubble Space Telescope',
            'aperture': 2.4,
            'site_code': 'orb-earth-low',
            'installation': 'HST',
            'tel_code': 'orb-earth-low.hst',
            'url': 'https://www.nasa.gov/mission_pages/hubble/main/index.html',
            'operator': None},
            {'name': 'INTErnational Gamma-Ray Astrophysics Laboratory (INTEGRAL)',
            'aperture': None,
            'site_code': 'orb-earth',
            'installation': 'INTEGRAL',
            'tel_code': 'orb-earth.integral',
            'url': 'https://sci.esa.int/web/integral',
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
            {'name': 'Advanced Camera for Surveys (ACS)',
            'site_code': 'orb-earth-low',
            'tel_code': 'orb-earth-low.hst',
            'installation': 'Hubble Space Telescope',
            'telescope': 'Hubble',
            'wavelength': 'UV/Optical/NIR',
            'capabilities': ['Wide-field Imaging'],
            'url': 'https://www.spacetelescope.org/about/general/instruments/acs/'},
            {'name': 'Wide Field Camera 3 (WFC3)',
            'site_code': 'orb-earth-low',
            'tel_code': 'orb-earth-low.hst',
            'installation': 'Hubble Space Telescope',
            'telescope': 'Hubble',
            'wavelength': 'UV/Optical/NIR',
            'capabilities': ['Wide-field Imaging'],
            'url': 'https://www.spacetelescope.org/about/general/instruments/wfc3/'},
            {'name': 'Cosmic Origins Spectrgraph (COS)',
            'site_code': 'orb-earth-low',
            'tel_code': 'orb-earth-low.hst',
            'installation': 'Hubble Space Telescope',
            'telescope': 'Hubble',
            'wavelength': 'UV/Optical/NIR',
            'capabilities': ['Spectroscopy'],
            'url': 'https://www.nasa.gov/content/hubble-space-telescope-cosmic-origins-spectrograph'},
            {'name': 'Space Telescope Imaging Spectrograph (STIS)',
            'site_code': 'orb-earth-low',
            'tel_code': 'orb-earth-low.hst',
            'installation': 'Hubble Space Telescope',
            'telescope': 'Hubble',
            'wavelength': 'UV/Optical/NIR',
            'capabilities': ['Spectroscopy'],
            'url': 'https://www.nasa.gov/content/hubble-space-telescope-space-telescope-imaging-spectrograph'},
            {'name': 'Fine Guidance Sensors',
            'site_code': 'orb-earth-low',
            'tel_code': 'orb-earth-low.hst',
            'installation': 'Hubble Space Telescope',
            'telescope': 'Hubble',
            'wavelength': 'UV/Optical/NIR',
            'capabilities': ['Interferometry'],
            'url': 'https://www.nasa.gov/content/hubble-space-telescope-fine-guidance-sensors'},
            {'name': 'SPI',
            'site_code': 'orb-earth',
            'tel_code': 'orb-earth.integral',
            'installation': 'INTEGRAL',
            'telescope': 'INTErnational Gamma-Ray Astrophysics Laboratory (INTEGRAL)',
            'wavelength': 'Gamma ray',
            'capabilities': ['Spectrometry'],
            'url': 'https://sci.esa.int/web/integral/-/31175-instruments?section=spi'},
            {'name': 'IBIS',
            'site_code': 'orb-earth',
            'tel_code': 'orb-earth.integral',
            'installation': 'INTEGRAL',
            'telescope': 'INTErnational Gamma-Ray Astrophysics Laboratory (INTEGRAL)',
            'wavelength': 'Gamma ray',
            'capabilities': ['Imaging'],
            'url': 'https://sci.esa.int/web/integral/-/31175-instruments?section=ibis'},
            {'name': 'JEM-X',
            'site_code': 'orb-earth',
            'tel_code': 'orb-earth.integral',
            'installation': 'INTEGRAL',
            'telescope': 'INTErnational Gamma-Ray Astrophysics Laboratory (INTEGRAL)',
            'wavelength': 'X-ray',
            'capabilities': ['Imaging'],
            'url': 'https://sci.esa.int/web/integral/-/31175-instruments?section=jem-x'},
            {'name': 'OMC',
            'site_code': 'orb-earth',
            'tel_code': 'orb-earth.integral',
            'installation': 'INTEGRAL',
            'telescope': 'INTErnational Gamma-Ray Astrophysics Laboratory (INTEGRAL)',
            'wavelength': 'Optical',
            'capabilities': ['Imaging'],
            'url': 'https://sci.esa.int/web/integral/-/31175-instruments?section=omc'},
    ]

    return instruments
