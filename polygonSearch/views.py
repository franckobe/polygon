from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from http.cookies import SimpleCookie


def login_view(request):

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
                    c = SimpleCookie()
                    token = Token.objects.get(user=user)
                    resp = redirect('search')
                    resp.set_cookie('token', token.__str__())
                    return resp
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
    resp = redirect('login')
    resp.delete_cookie('token')
    return resp


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


@login_required(login_url='/polygonSearch/login')
def search_view(request):
    user = request.user
    token = Token.objects.get(user=user)
    return render(request, 'search.html', locals())


@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
@api_view(['GET'])
def user_view(request):
    users = User.objects.all()
    users_json = []
    for user in users:
        users_json.append({
            "username": user.username
        })
    return Response(users_json)

@permission_classes(IsAuthenticated)
def preferences_view(request):
    # if request.method == 'POST':
    return render(request, 'preferences.html', locals())


