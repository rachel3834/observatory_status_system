from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django_filters.views import FilterView
from django.views.generic.detail import DetailView
from oss.models import FacilityOperator, Site, Installation, Telescope
from oss.models import InstrumentCapabilities, Instrument, FacilityStatus

class TelescopeStatus():
    def __init__(self):
        self.name = None
        self.site = None
        self.status = None
        self.comment = None
        self.instruments = []

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

            tel_states = get_status_for_telescopes(site, telescopes)

            site_status.append( tel_states )


        #context['tel_states'] = [tel_states[i] for (v, i) in sorted((v, i) for (i, v) in enumerate(tel_names)) ]
        context['site_states'] = zip(site_names, site_ids, site_status)

        return context

def get_status_for_telescopes(site, telescopes):
    tel_names = []
    tel_states = []

    for tel in telescopes:

        if tel.site == site:
            tel_stat = TelescopeStatus()
            tel_stat.name = tel.installation.name+' '+tel.name
            tel_stat.site = tel.site.name
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
                        tel_stat.instruments.append( (detector.name, status.status, status.comment) )
                    except FacilityStatus.DoesNotExist:
                        tel_stat.instruments.append( (detector.name, 'Unknown', '') )

            tel_states.append(tel_stat)

    telescope_states = [tel_states[i] for (v, i) in sorted((v, i) for (i, v) in enumerate(tel_names))]

    return telescope_states

class SiteDetailView(DetailView):
    template_name = 'oss/site_summary.html'
    model = Site

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['tel_list'] = Telescope.objects.filter(site=self.object)
        context['tel_states'] = get_status_for_telescopes(self.object, context['tel_list'])
        return context
