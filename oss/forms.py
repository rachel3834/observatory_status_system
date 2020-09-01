from django import forms
from  .models import FacilityStatus, Telescope, Instrument

class SetTelescopeStatusForm(forms.Form):
    class Meta:
        model = FacilityStatus
        fields = '__all__'

    instrument = forms.ModelMultipleChoiceField(queryset=Instrument.objects.all(),
                                                label='Instrument')
    telescope = forms.ModelMultipleChoiceField(queryset=Telescope.objects.all(),
                                                label='Telescope')
    states = (
                ('Open', 'Open'),
                ('Closed-weather', 'Closed - weather'),
                ('Closed-unsafe-to-observe', 'Closed - site conditions unsafe for observations'),
                ('Closed-daytime', 'Closed - outside operational period'),
                ('Offline', 'Offline - engineering'),
                ('Unknown', 'Unknown or unrecognised status')
                )
    status = forms.ChoiceField(label='Status', choices=states)
    status_start = forms.DateTimeField(label='DateTime status begins')
    status_end = forms.DateTimeField(label='DateTime status ends')
    comment = forms.CharField(label='Comment', max_length=300)
    last_updated = forms.DateTimeField(label='DateTime of last update')
