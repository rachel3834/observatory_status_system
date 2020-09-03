from .models import Site, Telescope, Instrument, FacilityStatus
from rest_framework import serializers
from django.db.models import F

class FacilityStatusSerializer(serializers.HyperlinkedModelSerializer):
    site = serializers.SerializerMethodField()
    site_id = serializers.SerializerMethodField()
    telescope = serializers.SerializerMethodField()
    telescope_id = serializers.SerializerMethodField()
    instrument = serializers.SerializerMethodField()
    instrument_id = serializers.SerializerMethodField()

    class Meta:
        model = FacilityStatus
        fields = ('site', 'site_id',
                  'telescope', 'telescope_id',
                  'instrument', 'instrument_id',
                  'status', 'status_start', 'status_end', 'comment')

    def get_site(self, obj):
        if obj.telescope.site:
            return obj.telescope.site.name
        elif obj.instrument.site:
            return obj.instrument.site.name
        else:
            return None

    def get_site_id(self, obj):
        if obj.telescope.site:
            return obj.telescope.site.pk
        elif obj.instrument.site:
            return obj.instrument.site.pk
        else:
            return None

    def get_telescope(self, obj):
        if obj.telescope:
            return obj.telescope.name
        else:
            return None

    def get_telescope_id(self, obj):
        if obj.telescope:
            return obj.telescope.pk
        else:
            return None

    def get_instrument(self, obj):
        if obj.instrument:
            return obj.instrument.name
        else:
            return None

    def get_instrument_id(self, obj):
        if obj.instrument:
            return obj.instrument.pk
        else:
            return None
