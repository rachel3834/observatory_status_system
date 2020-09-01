from django import forms
from  .models import FacilityStatus

class SetTelescopeStatusForm(forms.Form):
    class Meta:
        model = FacilityStatus
        fields = '__all__'
