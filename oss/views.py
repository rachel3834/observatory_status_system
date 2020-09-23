from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django_filters.views import FilterView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from oss.models import Site, Installation, Telescope
from oss.models import InstrumentCapabilities, Instrument, FacilityStatus
from .forms import SetTelescopeStatusForm
from rest_framework import viewsets
from rest_framework import permissions
from oss.serializers import FacilityStatusSerializer
from datetime import datetime, timedelta
import pytz
from itertools import chain

class LandingView(DetailView):

    def get(self, request):
        return render(request, 'oss/landing_page.html', {})

class AboutView(DetailView):

    def get(self, request):
        return render(request, 'oss/about.html', {})

class TelescopeStatus():
    def __init__(self):
        self.name = None
        self.site = None
        self.telescope = None
        self.status = None
        self.comment = None
        self.instruments = []
        self.timeline = []

class FacilityListView(FilterView):
    template_name = 'oss/facilities_list.html'
    paginate_by = 25
    strict = False
    model = Telescope

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        sites = Site.objects.all().order_by('name')

        telescopes = Telescope.objects.all()

        site_names = []
        site_ids = []
        site_status = []
        for site in sites:
            site_names.append(site.name)
            site_ids.append(site.pk)

            tel_states = get_current_status_for_telescopes(site, telescopes)

            site_status.append( tel_states )

        #context['tel_states'] = [tel_states[i] for (v, i) in sorted((v, i) for (i, v) in enumerate(tel_names)) ]
        context['site_states'] = zip(site_names, site_ids, site_status)

        return context

def get_current_status_for_telescopes(site, telescopes):
    tel_names = []
    tel_states = []

    for tel in telescopes:

        if tel.site == site:
            tel_stat = TelescopeStatus()
            tel_stat.name = tel.installation.name+' '+tel.name
            tel_stat.site = tel.site.name
            tel_stat.telescope = tel
            tel_names.append(tel.name)

            instruments = Instrument.objects.filter(telescope=tel)

            try:
                status = FacilityStatus.objects.filter(telescope=tel).latest('last_updated')
                tel_stat.status = status.status
                tel_stat.comment = status.comment
            except FacilityStatus.DoesNotExist:
                tel_stat.status = 'Unknown'
                tel_stat.comment = ''

            if len(instruments) > 0:

                for detector in instruments:
                    try:
                        status = FacilityStatus.objects.filter(instrument=detector).latest('last_updated')
                        tel_stat.instruments.append( (detector.name, status.status, status.comment, detector.pk) )
                    except FacilityStatus.DoesNotExist:
                        tel_stat.instruments.append( (detector.name, 'Unknown', '', detector.pk) )

            tel_states.append(tel_stat)

    telescope_states = [tel_states[i] for (v, i) in sorted((v, i) for (i, v) in enumerate(tel_names))]

    return telescope_states

def get_status_timeline_for_telescope(telescope):

    tel_status = get_current_status_for_telescopes(telescope.site, [telescope])[0]

    qs = FacilityStatus.objects.filter(telescope=telescope).order_by('status_start')

    dt = timedelta(days=1.0)

    timeline = []
    for entry in qs:
        if entry.status_end and entry.status_start != entry.status_end:
            date_range = entry.status_end - entry.status_start
            date_range = [entry.status_start + timedelta(days=x) for x in range(date_range.days+1)]
            for d in date_range:
                d = d.replace(tzinfo=pytz.UTC)
                timeline = add_entry_to_timeline( (d, entry.status, entry.last_updated), timeline )
        else:
            timeline = add_entry_to_timeline( (entry.status_start, entry.status, entry.last_updated), timeline )

    tel_status.timeline = timeline

    return tel_status

def add_entry_to_timeline(new_entry, timeline):

    idx = None
    for i, entry in enumerate(timeline):
        if entry[0] == new_entry[0]:
            if new_entry[2] >= entry[2]:
                idx = i
            else:
                idx = -1
    if idx == None:
        timeline.append(new_entry)
    elif idx > -1:
        timeline[idx] = new_entry

    return timeline

class SiteDetailView(DetailView):
    template_name = 'oss/site_summary.html'
    model = Site

    ## Possible upgrade: embed google map showing site location

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['tel_list'] = Telescope.objects.filter(site=self.object)
        context['tel_states'] = get_current_status_for_telescopes(self.object, context['tel_list'])
        return context

class TelescopeDetailView(DetailView):
    template_name = 'oss/telescope_summary.html'
    model = Telescope

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['site'] = Site.objects.get(telescope=self.object)
        context['installation'] = Installation.objects.get(telescope=self.object)
        instruments = Instrument.objects.filter(telescope=self.object)
        instrument_list = []
        for instrument in instruments:
            capabilities = InstrumentCapabilities.objects.filter(instrument=instrument)
            description = ''
            for cap in capabilities:
                if len(description) > 0:
                    description += ', '+cap.descriptor
                else:
                    description += cap.descriptor
            instrument_list.append( (instrument, description) )
        context['instrument_list'] = instrument_list
        context['tel_state'] = get_status_timeline_for_telescope(self.object)
        return context

class InstrumentDetailView(DetailView):
    template_name = 'oss/instrument_summary.html'
    model = Instrument

    ## Possible upgrade: embed google map showing site location

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['telescope'] = self.object.telescope
        capabilities = InstrumentCapabilities.objects.filter(instrument=self.object)
        description = ''
        for cap in capabilities:
            if len(description) > 0:
                description += ', '+cap.descriptor
            else:
                description += cap.descriptor
        context['description'] = description
        return context

class FacilityStatusCreate(LoginRequiredMixin, FormView):
    template_name = 'oss/set_facility_status.html'
    form_class = SetTelescopeStatusForm
    success_url =reverse_lazy('facilities_list')

    def form_valid(self, form):
        status = FacilityStatus.objects.create(telescope=form.cleaned_data['telescope'][0],
                                              instrument=form.cleaned_data['instrument'][0],
                                                status=form.cleaned_data['status'],
                                                status_start=form.cleaned_data['status_start'],
                                                status_end=form.cleaned_data['status_end'],
                                                comment=form.cleaned_data['comment'],
                                                last_updated=form.cleaned_data['last_updated'])
        return super().form_valid(form)


## Add content of other observatorys
# Management commands to fetch status of other facilities
## http://www-kpno.kpno.noao.edu/weather.shtml
## ALMA
## ATCA twitter feed: https://twitter.com/jamie_atca_sss
## ATLAS dashboards: http://dashboard.fallingstar.com/dash/mlo.html

## Status information in the past - how do I handle multiple status updates in one day?
