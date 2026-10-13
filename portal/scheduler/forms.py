from django import forms

from .models import Meeting


def _datetime_field(label):
    # a datetime-local input shows AM/PM in US-locale browsers, so split it into
    # a date picker plus a plain 24h "HH:MM" text box
    return forms.SplitDateTimeField(
        label=label,
        input_time_formats=['%H:%M'],
        widget=forms.SplitDateTimeWidget(
            date_attrs={'type': 'date'},
            time_attrs={
                'placeholder': 'HH:MM',
                'pattern': r'([01]?\d|2[0-3]):[0-5]\d',
                'title': '24-hour time, e.g. 14:30',
                'inputmode': 'numeric',
                'size': 5,
            },
            date_format='%Y-%m-%d',
            time_format='%H:%M',
        ),
    )


class MeetingForm(forms.ModelForm):
    start = _datetime_field('Start')
    end = _datetime_field('End')

    class Meta:
        model = Meeting
        fields = ['title', 'start', 'end', 'attendees', 'comment']
        widgets = {
            'attendees': forms.SelectMultiple(),
            'comment': forms.Textarea(attrs={'rows': 4}),
        }
