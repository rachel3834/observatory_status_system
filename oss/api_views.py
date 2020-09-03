from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django_filters.views import FilterView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from oss.models import Site, Installation, Telescope
from oss.models import InstrumentCapabilities, Instrument, FacilityStatus
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from oss.serializers import FacilityStatusSerializer
from datetime import datetime, timedelta
import pytz

class FacilityStatusView(APIView):
    """View handling publicly-accessible facility status functions.
    Allows list only."""

    def get(self, request, format=None):
        queryset = FacilityStatus.objects.all().order_by('last_updated')
        serializer = FacilityStatusSerializer(queryset, many=True)
        return Response(serializer.data)

class UpdateFacilityStatusView(LoginRequiredMixin, viewsets.ModelViewSet):
    """View handling Facility Status.  Allows list and create"""
    queryset = FacilityStatus.objects.all().order_by('last_updated')
    serializer_class = FacilityStatusSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):

        keys = [ 'telescope','instrument','status','status_start',
                'status_end','comment','last_updated']
        state = {}
        for key in keys:
            if key in request.data.keys():
                state[key] = request.data[key]

        if 'telescope' in state:
            state['telescope'] = Telescope.objects.get(pk=int(state['telescope']))
        elif 'instrument' in state:
            state['instrument'] = Instrument.objects.get(pk=int(state['instrument']))

        try:
            FacilityStatus.objects.create(**state)
        except Telescope.DoesNotExist:
            pass

        response = super().create(request, *args, **kwargs)
        return response
