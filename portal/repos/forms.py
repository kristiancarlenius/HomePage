from django import forms

from .models import RepoLink


class RepoLinkForm(forms.ModelForm):
    class Meta:
        model = RepoLink
        fields = ['name', 'url', 'tag', 'description']
        widgets = {'description': forms.Textarea(attrs={'rows': 3})}
