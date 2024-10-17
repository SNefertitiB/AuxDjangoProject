#from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.shortcuts import render, redirect
from .forms import UserCreationForm, SignupForm
from django.contrib.auth import authenticate, login
from WhosOnAux.views import user_home
from django.contrib import messages


# Create your views here.
# class SignUpView(CreateView):
#     form_class = UserCreationForm
#     success_url = reverse_lazy("login")
#     template_name = "registration/signup.html"

def signup(request):
    # TODO: error message if username or email has already been used
    form = SignupForm(request.POST)
    if request.user.is_authenticated:
        return redirect('user_home')
    else:
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            form.save()
            new_user = authenticate(username=username, password=password)
            if new_user is not None:
                messages.success(request, 'Your account has been created successfully.')
                login(request, new_user)
                return redirect("user_home")

        else:
            messages.info(request, 'invalid registration details')
    context = {
        'form': form,
    }
    return render(request, 'registration/signup.html', context)
