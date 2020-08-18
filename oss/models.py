from django.db import models
from django.utils import timezone

# Create your models here.
class FacilityOperator(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField("Operator Name", max_length=50)
    email = models.EmailField("Email")
    institution = models.CharField("Institution", max_length=50)

class Site(models.Model):
    def __str__(self):
        return self.name

    location_options = ( ('Ground-based', 'Ground-based'),
                          ('Space', 'Space') )
    orbit_options = (
            ('Earth orbit', 'Earth orbit'),
            ('L2', 'L2'),
            ('Earth-trailing', 'Earth-trailing'),
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

class Installation(models.Model):
    def __str__(self):
        return self.name
    installation_options = (
        ('Dome', 'Dome'),
        ('Dish', 'Dish'),
        ('Enclosure', 'Enclosure'),
        ('Array', 'Array'),
        ('Spacecraft', 'Spacecraft')
    )
    name = models.CharField("Installation Name", max_length=50)
    type = models.CharField("Type", max_length=30, choices=installation_options,
                            default='Dome', null=True, blank=True)
    site = models.ForeignKey(Site, on_delete=models.PROTECT)

class Telescope(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField("Telescope Name", max_length=50)
    aperture = models.DecimalField("Telescope Effective Aperture (m)", max_digits=6,
                                  decimal_places=2, null=True, blank=True)
    operator = models.ForeignKey(FacilityOperator, on_delete=models.PROTECT)
    site = models.ForeignKey(Site, on_delete=models.PROTECT)
    installation = models.ForeignKey(Installation, on_delete=models.PROTECT)

class InstrumentCapabilities(models.Model):
    def __str__(self):
        return self.descriptor
    descriptor_options = (
            ('Imaging', 'Imaging'),
            ('Long-slit spectroscopy', 'Long-slit spectroscopy'),
            ('Fiber-fed spectroscopy', 'Fiber-fed spectroscopy'),
            ('Echelle spectroscopy', 'Echelle spectroscopy'),
            ('Polarimetry', 'Polarimetry'),
            ('Interferometry', 'Interferometry'),

    )
    descriptor = models.CharField("Description of capability", max_length=50)

class Instrument(models.Model):
    def __str__(self):
        return self.name

    wavelength_options = (
          ('Optical', 'Optical'),
          ('IR', 'Infrared'),
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
    capabilities = models.ManyToManyField(InstrumentCapabilities,
                                null=True, blank=True)

class FacilityStatus(models.Model):
    def __str__(self):
        return self.status

    states = (
                ('Open', 'Open'),
                ('Closed-weather', 'Closed - weather'),
                ('Closed-daytime', 'Closed - outside operational period'),
                ('Offline', 'Offline - engineering')
                )
    status = models.CharField("Status", max_length=50)
    status_start = models.DateTimeField('DateTime status begins')
    status_end = models.DateTimeField('DateTime status ends',
                                null=True, blank=True)
    last_updated = models.DateTimeField('DateTime of last update')
