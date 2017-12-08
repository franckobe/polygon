from django import forms


class ConnexionForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", max_length=30)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    username = forms.CharField(label="Saisir votre nom d'utilisateur", max_length=30, min_length=8)
    password = forms.CharField(label="Saisir votre mot de passe (8 caractères minimum)", max_length=30, min_length=8)
    passwordVerif = forms.CharField(label="Contrôle du mot de passe (saisir le même mot de passe", max_length=30, min_length=8)

