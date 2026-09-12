from django import forms

from .models import Meeting


class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ['title', 'start', 'end', 'attendees', 'comment']
        widgets = {
            'start': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'attendees': forms.SelectMultiple(),
            'comment': forms.Textarea(attrs={'rows': 4}),
        }
