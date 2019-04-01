from django.forms import ModelForm
from .models import RhPlan, Member

class RhPlanForm(ModelForm):
    class Meta:
        model = RhPlan
        fields = ['plan', 'log']

"""
class TeamForm(ModelForm):
    def __init__(self, memberQueryset=None, *args, **kwargs):
        super(TeamForm, self).__init__(*args, **kwargs)
        if memberQueryset:
            self.fields['member'].queryset = memberQueryset
"""
