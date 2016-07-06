from django import forms


class UrlForm(forms.Form):
    original_url = forms.URLField(label='Paste your long URL here:')
