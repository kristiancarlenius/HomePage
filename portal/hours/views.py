import csv

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import staff_required

from .forms import TimeEntryForm
from .models import TimeEntry


@login_required
def my_hours(request):
    entries = TimeEntry.objects.filter(user=request.user)
    total = entries.aggregate(total=Sum('hours'))['total'] or 0
    return render(request, 'hours/my_hours.html', {'entries': entries, 'total': total})


@login_required
def entry_create(request):
    if request.method == 'POST':
        form = TimeEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            messages.success(request, 'Hours logged.')
            return redirect('my_hours')
    else:
        form = TimeEntryForm()
    return render(request, 'hours/entry_form.html', {'form': form})


@login_required
def entry_edit(request, pk):
    entry = get_object_or_404(TimeEntry, pk=pk)
    if entry.user_id != request.user.id and not request.user.is_staff:
        raise PermissionDenied('You can only edit your own hours.')
    if request.method == 'POST':
        form = TimeEntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            messages.success(request, 'Entry updated.')
            return redirect('my_hours')
    else:
        form = TimeEntryForm(instance=entry)
    return render(request, 'hours/entry_form.html', {'form': form, 'entry': entry})


@login_required
def entry_delete(request, pk):
    entry = get_object_or_404(TimeEntry, pk=pk)
    if entry.user_id != request.user.id and not request.user.is_staff:
        raise PermissionDenied('You can only delete your own hours.')
    if request.method == 'POST':
        entry.delete()
        messages.success(request, 'Entry deleted.')
        return redirect('my_hours')
    return render(request, 'hours/entry_confirm_delete.html', {'entry': entry})


def _billing_queryset(request):
    qs = TimeEntry.objects.select_related('user', 'customer')
    start = request.GET.get('start')
    end = request.GET.get('end')
    if start:
        qs = qs.filter(date__gte=start)
    if end:
        qs = qs.filter(date__lte=end)
    return qs, start, end


@staff_required
def billing(request):
    qs, start, end = _billing_queryset(request)
    rollup = (
        qs.values('user__username', 'customer__name')
        .annotate(total_hours=Sum('hours'))
        .order_by('user__username', 'customer__name')
    )
    grand_total = qs.aggregate(total=Sum('hours'))['total'] or 0
    return render(
        request,
        'hours/billing.html',
        {'rollup': rollup, 'grand_total': grand_total, 'start': start or '', 'end': end or ''},
    )


@staff_required
def billing_csv(request):
    qs, start, end = _billing_queryset(request)
    rollup = (
        qs.values('user__username', 'customer__name')
        .annotate(total_hours=Sum('hours'))
        .order_by('user__username', 'customer__name')
    )
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="billing.csv"'
    writer = csv.writer(response)
    writer.writerow(['User', 'Customer', 'Total hours'])
    for row in rollup:
        writer.writerow([row['user__username'], row['customer__name'] or '', row['total_hours']])
    return response
