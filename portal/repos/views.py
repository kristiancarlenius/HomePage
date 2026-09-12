from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RepoLinkForm
from .models import RepoLink


@login_required
def repo_list(request):
    repos = RepoLink.objects.all()
    return render(request, 'repos/repo_list.html', {'repos': repos})


@login_required
def repo_create(request):
    if request.method == 'POST':
        form = RepoLinkForm(request.POST)
        if form.is_valid():
            repo = form.save(commit=False)
            repo.added_by = request.user
            repo.save()
            messages.success(request, 'Repo added.')
            return redirect('repo_list')
    else:
        form = RepoLinkForm()
    return render(request, 'repos/repo_form.html', {'form': form})


@login_required
def repo_edit(request, pk):
    repo = get_object_or_404(RepoLink, pk=pk)
    if request.method == 'POST':
        form = RepoLinkForm(request.POST, instance=repo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Repo updated.')
            return redirect('repo_list')
    else:
        form = RepoLinkForm(instance=repo)
    return render(request, 'repos/repo_form.html', {'form': form, 'repo': repo})


@login_required
def repo_delete(request, pk):
    repo = get_object_or_404(RepoLink, pk=pk)
    if request.method == 'POST':
        repo.delete()
        messages.success(request, 'Repo removed.')
        return redirect('repo_list')
    return render(request, 'repos/repo_confirm_delete.html', {'repo': repo})
