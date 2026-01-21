from django import forms


class ScanAddForm(forms.Form):
    target = forms.IntegerField()
    tool = forms.IntegerField()
