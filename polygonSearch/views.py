from django.contrib.auth import authenticate, login , logout
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .form import *
from .models import User

# Create your views here.

from django.contrib.auth import authenticate, login

def connexion(request):

    if request.method == "POST":
        form = ConnexionForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)  # Nous vérifions si les données sont correctes
            if user:  # Si l'objet renvoyé n'est pas None
                login(request, user)  # nous connectons l'utilisateur
    else:
        form = ConnexionForm()

    return render(request, 'login.html', locals())

@login_required(login_url="/Login/")
def Index(request):
    return redirect('Index.html')

#@logout
def Logout(request):
    logout(request)
    return redirect('login.html')

def Register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data["username"]
            if form.password == form.passwordVerif:
                password = form.cleaned_data["password"]
        user = User(password = password, username = username)
        user.save()
    else:
        form = RegisterForm()

    return render(request, 'login.html', locals())



