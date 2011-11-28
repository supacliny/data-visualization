from django import forms

class SymbolForm(forms.Form):
    symbol = forms.CharField(max_length=4)
    fromdate = forms.DateField('%Y-%m-%d')
    todate = forms.DateField('%Y-%m-%d')
