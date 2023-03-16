from django import forms


class DateInput(forms.DateInput):
    input_type = "date"


class QueryForm(forms.Form):
    template_name = "webscrapper/form_snippet.html"
    region = forms.CharField(label='region', max_length=100)
    adults = forms.IntegerField(label='adults', initial=1)
    children = forms.IntegerField(label='children', initial=0)
    infants = forms.IntegerField(label='infants', initial=0)
    start = forms.DateField(label="start date", widget=DateInput())
    end = forms.DateField(label="end date", widget=DateInput())

