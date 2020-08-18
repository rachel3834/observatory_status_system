from django.contrib import admin
from oss.models import FacilityOperator, Site, Installation, Telescope
from oss.models import InstrumentCapabilities, Instrument, FacilityStatus

# Register your models here.
admin.site.register(FacilityOperator)
admin.site.register(Site)
admin.site.register(Installation)
admin.site.register(Telescope)
admin.site.register(InstrumentCapabilities)
admin.site.register(Instrument)
admin.site.register(FacilityStatus)
