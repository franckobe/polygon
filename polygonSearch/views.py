from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.auth.models import User


def login_view(request):
    next_url = 'login/'+request.GET.get('next') if request.GET.get('next') else 'login'

    if request.user.is_authenticated:
        return redirect('search')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            if username and password:
                user = authenticate(username=username, password=password)
                if user:
                    login(request, user)
                    return redirect('search')
                else:
                    error = 'La tentative de connexion a échoué !'
                    return render(request, 'login.html', locals())
            else:
                username_error = False if username else True
                password_error = False if password else True
                error = 'Vous devez saisir tous les champs !'
                return render(request, 'login.html', locals())
        else:
            return render(request, 'login.html', locals())


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')


@login_required(login_url='/polygonSearch/login')
def search_view(request):
    return render(request, 'search.html', locals())


def register_view(request):
    if request.user.is_authenticated:
        return redirect('search')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            password_confirmation = request.POST.get('password_confirmation')
            if username and password and password_confirmation:
                if password == password_confirmation:
                    user = User.objects.create_user(username=username)
                    if user:
                        user.set_password(password)
                        user.save()
                        return redirect('login')
                    else:
                        error = 'La tentative d\'inscription a échoué !'
                        return render(request, 'register.html', locals())
                else:
                    password_error = password_confirmation_error = False if password == password_confirmation else True
                    error = 'Les mots de passe doivent être identiques !'
                    return render(request, 'register.html', locals())
            else:
                username_error = False if username else True
                password_error = False if password else True
                password_confirmation_error = False if password_confirmation else True
                error = 'Vous devez saisir tous les champs !'
                return render(request, 'register.html', locals())
        else:
            return render(request, 'register.html', locals())
