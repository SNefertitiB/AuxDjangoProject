#from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.shortcuts import render, redirect
from .forms import UserCreationForm, SignupForm
from django.contrib.auth import authenticate, login
from WhosOnAux.views import user_home
from django.contrib import messages
from django.contrib.auth.models import User


# Create your views here.

def signup(request):
    if request.user.is_authenticated:
        return redirect('user_home')

    form = SignupForm(request.POST)
    context = {'form': form}

    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if not User.objects.filter(email=email).exists():
                form.save()
                new_user = User.objects.get(email=email)
                messages.success(request, 'Your account has been created successfully.')
                login(request, new_user)
                return redirect("user_home")
            else:
                messages.error(request,
                               'An account with that email already exists. Please log in or sign up with a different email')
        else:
            attempted_username = form.cleaned_data.get('username')
            if User.objects.filter(username=attempted_username).exists():
                messages.error(request, 'An account with that username already exists. Please log in or sign up with a different username')
            messages.error(request, 'invalid registration details')

    return render(request, 'registration/signup.html', context)

