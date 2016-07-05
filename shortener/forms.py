from django import forms


class UrlForm(forms.Form):
    original_url = forms.URLField()
    # shorten_url = forms.URLField()
    # date_add = forms.DateTimeField()
    # date_click = forms.DateTimeField()
    # clicks = forms.IntegerField()
