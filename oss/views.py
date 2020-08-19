from django.shortcuts import render
from django_filters.views import FilterView
from oss.models import FacilityOperator, Site, Installation, Telescope
from oss.models import InstrumentCapabilities, Instrument, FacilityStatus

class TelescopeStatus():
    def __init__(self):
        self.name = None
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

        telescopes = Telescope.objects.all()

        tel_states = []
        tel_names = []
        for tel in telescopes:

            tel_stat = TelescopeStatus()
            tel_stat.name = tel.name
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

        context['tel_states'] = [tel_states[i] for (v, i) in sorted((v, i) for (i, v) in enumerate(tel_names)) ] 

        return context
