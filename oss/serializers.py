from .models import Telescope, FacilityStatus
from rest_framework import serializers

class FacilityStatusSerializer(serializers.HyperlinkedModelSerializer):
    telescope = serializers.StringRelatedField()
    instrument = serializers.StringRelatedField()
    class Meta:
        model = FacilityStatus
        fields = ['telescope', 'instrument', 'status_start', 'status_end', 'status', 'comment']
