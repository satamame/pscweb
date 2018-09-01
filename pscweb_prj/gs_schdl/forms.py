from django.forms import ModelForm
from .models import RhPlan

class RhPlanForm(ModelForm):
    class Meta:
        model = RhPlan
        fields = ['plan', 'log']
