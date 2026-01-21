from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/targets/')
    else:
        form = UserCreationForm()

    for field in form.fields:
     form.fields[field].widget.attrs.update({
        'class': 'form-control'
    })
    
    return render(request, 'accounts/register.html', {'form': form})
