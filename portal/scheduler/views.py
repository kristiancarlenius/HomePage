from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.dateparse import parse_datetime
from django.http import JsonResponse

from .forms import MeetingForm
from .models import Meeting


@login_required
def calendar_view(request):
    return render(request, 'scheduler/calendar.html')


@login_required
def events_json(request):
    # fullcalendar re-fetches this whenever the visible range changes
    qs = Meeting.objects.all()
    start = parse_datetime(request.GET.get('start', ''))
    end = parse_datetime(request.GET.get('end', ''))
    if start and end:
        qs = qs.filter(start__lt=end, end__gt=start)

    events = [
        {
            'id': m.id,
            'title': m.title,
            'start': m.start.isoformat(),
            'end': m.end.isoformat(),
            'url': reverse('meeting_edit', args=[m.id]),
            'extendedProps': {
                'comment': m.comment,
                'attendees': ', '.join(u.get_full_name() or u.username for u in m.attendees.all()),
            },
        }
        for m in qs
    ]
    return JsonResponse(events, safe=False)


@login_required
def meeting_create(request):
    if request.method == 'POST':
        form = MeetingForm(request.POST)
        if form.is_valid():
            meeting = form.save(commit=False)
            meeting.created_by = request.user
            meeting.save()
            form.save_m2m()
            messages.success(request, 'Meeting created.')
            return redirect('calendar')
    else:
        form = MeetingForm()
    return render(request, 'scheduler/meeting_form.html', {'form': form})


@login_required
def meeting_edit(request, pk):
    meeting = get_object_or_404(Meeting, pk=pk)
    if not meeting.can_edit(request.user):
        raise PermissionDenied('Only the meeting creator or an admin can edit this meeting.')
    if request.method == 'POST':
        form = MeetingForm(request.POST, instance=meeting)
        if form.is_valid():
            form.save()
            messages.success(request, 'Meeting updated.')
            return redirect('calendar')
    else:
        form = MeetingForm(instance=meeting)
    return render(request, 'scheduler/meeting_form.html', {'form': form, 'meeting': meeting})


@login_required
def meeting_delete(request, pk):
    meeting = get_object_or_404(Meeting, pk=pk)
    if not meeting.can_edit(request.user):
        raise PermissionDenied('Only the meeting creator or an admin can delete this meeting.')
    if request.method == 'POST':
        meeting.delete()
        messages.success(request, 'Meeting deleted.')
        return redirect('calendar')
    return render(request, 'scheduler/meeting_confirm_delete.html', {'meeting': meeting})
