from django.db import models
from django.utils import timezone
from django.conf import settings

class Site(models.Model):
    def __str__(self):
        return self.name

    location_options = ( ('Ground-based', 'Ground-based'),
                          ('Space', 'Space') )
    orbit_options = (
            ('Earth orbit', 'Earth orbit'),
            ('L2', 'L2'),
            ('Earth-trailing', 'Earth-trailing'),
            ('Equatorial Earth orbit', 'Equatorial Earth orbit'),
            ('LEO', 'Low Earth orbit'),
            ('Mars orbit', 'Mars orbit'),
            ('Outbound trajectory', 'Outbound trajectory')
                    )
    name = models.CharField("Operator Name", max_length=50)
    location = models.CharField("Location", max_length=30, choices=location_options,
                            default='Ground-based', null=True, blank=True)
    latitude = models.DecimalField("Latitude (N) in decimal degrees",
                                  max_digits=8, decimal_places=4, null=True,
				                  blank=True)
    longitude = models.DecimalField("Longitude (E) in decimal degrees",
                                   max_digits=8, decimal_places=4, null=True,
				                   blank=True)
    altitude = models.DecimalField("Altitude (m)", max_digits=8,
                                    decimal_places=4, null=True, blank=True)
    orbit = models.CharField("Orbit", max_length=30, choices=orbit_options,
                            null=True, blank=True)
    site_code = models.CharField("Site code", max_length=10, null=True, blank=True)
    url = models.URLField(max_length=200, null=True, blank=True)

class Installation(models.Model):
    def __str__(self):
        return self.name+' '+self.site.name
    installation_options = (
        ('Dome', 'Dome'),
        ('Dish', 'Dish'),
        ('Enclosure', 'Enclosure'),
        ('Array', 'Array'),
        ('Spacecraft', 'Spacecraft'),
    )
    name = models.CharField("Installation Name", max_length=50)
    type = models.CharField("Type", max_length=30, choices=installation_options,
                            default='Dome', null=True, blank=True)
    site = models.ForeignKey(Site, on_delete=models.PROTECT)

class Telescope(models.Model):
    def __str__(self):
        return self.name+' '+self.installation.name+' '+self.site.name

    name = models.CharField("Telescope Name", max_length=50)
    tel_code = models.CharField("Telescope code", max_length=50, null=True, blank=True)
    aperture = models.DecimalField("Telescope Effective Aperture (m)", max_digits=6,
                                  decimal_places=2, null=True, blank=True)
    operator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True)
    site = models.ForeignKey(Site, on_delete=models.PROTECT)
    installation = models.ForeignKey(Installation, on_delete=models.PROTECT)
    url = models.URLField(max_length=200, null=True, blank=True)

class InstrumentCapabilities(models.Model):
    def __str__(self):
        return self.descriptor
    descriptor = models.CharField("Description of capability", max_length=50)

class Instrument(models.Model):
    def __str__(self):
        return self.name+' '+self.telescope.name+' '+self.telescope.site.name

    wavelength_options = (
          ('Optical', 'Optical'),
          ('IR', 'Infrared'),
          ('Optical/NIR', 'Optical/Infrared'),
          ('Millimeter', 'Millimeter'),
          ('Microwave', 'Microwave'),
          ('Radio', 'Radio'),
          ('UV', 'UV'),
          ('Gamma ray', 'Gamma ray'),
          ('X-ray', 'X-ray'),
          ('Gravitational waves', 'Gravitational waves'),
          ('Neutrinos', 'Neutrinos')
          )

    name = models.CharField("Instrument Name", max_length=50)
    wavelength = models.CharField("Wavelength range/messenger", max_length=30, choices=wavelength_options,
      default='Optical', null=True, blank=True)
    capabilities = models.ManyToManyField(InstrumentCapabilities, blank=True)
    telescope = models.ForeignKey(Telescope, on_delete=models.PROTECT, blank=True, null=True)
    url = models.URLField(max_length=200, null=True, blank=True)

class FacilityStatus(models.Model):
    def __str__(self):
        try:
            return self.instrument.name+' '+self.status
        except AttributeError:
            return self.telescope.tel_code+' '+self.status

    states = (
                ('Open', 'Open'),
                ('Closed-weather', 'Closed - weather'),
                ('Closed-unsafe-to-observe', 'Closed - site conditions unsafe for observations'),
                ('Closed-daytime', 'Closed - outside operational period'),
                ('Offline', 'Offline - engineering'),
                ('Unknown', 'Unknown or unrecognised status')
                )
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE, blank=True, null=True)
    telescope = models.ForeignKey(Telescope, on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField("Status", max_length=50, choices=states)
    status_start = models.DateTimeField('DateTime status begins')
    status_end = models.DateTimeField('DateTime status ends',
                                null=True, blank=True)
    comment = models.CharField("Status", max_length=300, blank=True, null=True)
    last_updated = models.DateTimeField('DateTime of last update')
