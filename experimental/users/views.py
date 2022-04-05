from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegister

def register(req):
    if req.method == 'POST':
        form = UserRegister(req.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.info(req, f'Details: {username}')
            return redirect("login")
    else:
        form = UserRegister()
    return render(req, 'users/register.html', {'form': form})
