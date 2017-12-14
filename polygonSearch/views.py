from django.contrib.auth import authenticate, login , logout
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .form import *
from .models import User
from django.contrib.auth import authenticate, login
from django.contrib.admin.views.decorators import staff_member_required


# Create your views here.
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


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data["username"]
            if form.password == form.passwordVerif:
                password = form.cleaned_data["password"]
                user = User(password=password, username=username)
                user.save()
    else:
        form = RegisterForm()

    return render(request, 'login.html', locals())

@staff_member_required
def del_user(request, username):
    try:
        u = User.objects.get(username = username)
        u.delete()
        messages.sucess(request, "The user is deleted")

    #ToDo ne pas renvoyer sur la page Index mais sur la page d'acceuil de l'admin
    #Todo A créer page d'admin
    #ToDo Implémenter ListeUser pour la suppression
    except User.DoesNotExist:
        messages.error(request, "User doesnot exist")
        return render(request, 'index.html')
    # ToDo ne pas renvoyer sur la page Index mais sur la page d'acceuil de l'admin
    except Exception as e:
        return render(request, 'index.html',{'err':e.message})

    # ToDo ne pas renvoyer sur la page Index mais sur la page d'acceuil de l'admin
    return render(request, 'index.html')

def edit_user(request):
        if request.method == "POST":
            form = EditForm(data=request.POST, instance=request.user)
            if form.is_valid():
                form.save()
        else:
            form = EditForm()
        # Todo A créer page d'admin
        return render(request,'index.html' ,locals())



