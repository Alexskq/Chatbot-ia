from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from datetime import datetime

# Create your views here.

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Compte créé pour {username}! Vous pouvez maintenant vous connecter.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    context = {
        'user': request.user,
    }
    return render(request, 'registration/profile.html', context)

def test_view(request):
    context = {
        'current_date': datetime.now(),
        'user': request.user,
    }
    return render(request, 'test.html', context)
