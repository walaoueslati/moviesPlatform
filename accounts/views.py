from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegistrationForm


def register(request):
    if request.user.is_authenticated:
        return render(request, "accounts/register.html", {"message": "You are already logged in. Please log out to register a new account."})
    
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)

            login(request, user)

            return redirect("movies:home")
    else:
        form = RegistrationForm()

    return render(request, "accounts/register.html", {"form": form})

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            login(request, user)
            return redirect('home')  
        else:
            return render(request, 'accounts/login.html', {"error": "Identifiant ou mot de passe invalide."})

    return render(request, 'accounts/login.html')

def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("accounts:login") 
    else:
        return redirect("accounts:login")
