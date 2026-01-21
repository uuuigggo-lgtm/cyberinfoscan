from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Target
from .forms import TargetForm

@login_required
def target_list(request):
    targets = Target.objects.filter(owner=request.user)
    return render(request, 'targets/list.html', {'targets': targets})


@login_required
def target_add(request):
    if request.method == 'POST':
        form = TargetForm(request.POST)
        if form.is_valid():
            target = form.save(commit=False)
            target.owner = request.user
            target.save()
            return redirect('targets:list')
    else:
        form = TargetForm()

    return render(request, 'targets/add.html', {'form': form})

@login_required
def target_edit(request, pk):
    target = get_object_or_404(Target, pk=pk, owner=request.user)
   
   
    if request.method == 'POST':
        target.name = request.POST.get('name')
        target.target_type = request.POST.get('target_type')
        target.save()
        return redirect('targets:list')
    return render(request, 'targets/edit.html', {'target': target})


@login_required
def target_delete(request, pk):
    target = get_object_or_404(Target, pk=pk, owner=request.user)
    if request.method == 'POST':
        target.delete()
        return redirect('targets:list')
    return render(request, 'targets/delete.html', {'target': target})
