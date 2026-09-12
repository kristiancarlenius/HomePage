from django import forms

from .models import Customer


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'contact_info', 'rate', 'projects_done', 'potential_needs', 'known_issues', 'notes']
        widgets = {
            'contact_info': forms.Textarea(attrs={'rows': 3}),
            'projects_done': forms.Textarea(attrs={'rows': 4}),
            'potential_needs': forms.Textarea(attrs={'rows': 4}),
            'known_issues': forms.Textarea(attrs={'rows': 4}),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }
