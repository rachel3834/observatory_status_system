from .models import Telescope
from rest_framework import serializers

class TelescopeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Telescope
        fields = ['name', 'tel_code', 'site']
