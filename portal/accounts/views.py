from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .decorators import staff_required
from .forms import AdminUserCreateForm


@login_required
def dashboard(request):
    return render(request, 'accounts/dashboard.html')


@staff_required
def user_create(request):
    if request.method == 'POST':
        form = AdminUserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Account created for {user.username}.')
            return redirect('user_create')
    else:
        form = AdminUserCreateForm()
    return render(request, 'accounts/user_form.html', {'form': form})
