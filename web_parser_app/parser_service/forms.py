from django import forms
from .models import PersonSettings


class PersonSettingsForm(forms.ModelForm):
    class Meta:
        model = PersonSettings
        fields = ['words_file', 'min_view_count', 'shorts', 'max_sub_count', 'proxy_address', 'proxy_login', 'proxy_pass', 'mode']
