from django.shortcuts import render
from oss.models import FacilityOperator, Site, Installation, Telescope
from oss.models import InstrumentCapabilities, Instrument, FacilityStatus

# Create your views here.
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world!")

class FacilityListView():
    template_name = 'oss/facilities_list.html'
    paginate_by = 25
    strict = False
    model = Telescope

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['telescope_count'] = context['paginator'].count
        # hide target grouping list if user not logged in
        context['facilities'] = Telescope.objects.all()
        return context
