from django import forms
from .models import Target


class TargetForm(forms.ModelForm):

    TARGET_TYPES = [
        ('domain', 'Domain'),
        ('ip', 'IP Address'),
        ('url', 'URL'),
    ]

    target_type = forms.ChoiceField(
        choices=TARGET_TYPES,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )

    class Meta:
        model = Target
        fields = ['name', 'target_type']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'example.com or 192.168.1.1'
            }),
        }
