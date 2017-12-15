from django.db import models
from django.contrib.auth.models import User

'''
python manage.py makemigrations
python manage.py migrate

si migrate ne fonctionne pas : 
- Vider la table django_migrations
- Supprimer le dossier migrations
- Executer le makemigrations
- python manage.py migrate --fake-initial
'''
class Website_domain(models.Model):
    id_website_domain   = models.AutoField(primary_key=True)
    name                = models.CharField(max_length=50)
    is_allowed          = models.IntegerField(default=-1)
    id_owner            = models.ForeignKey('Website_owner', on_delete=models.CASCADE, default=-1)


class Website_word(models.Model):
    id_website_word     = models.AutoField(primary_key=True)
    word                = models.CharField(max_length=50)
    weight              = models.IntegerField(default=1)
    url                 = models.CharField(max_length=255)


class Website_page(models.Model):
    id_website_page     = models.AutoField(primary_key=True)
    url                 = models.CharField(max_length=255)
    title               = models.CharField(max_length=50)
    content             = models.TextField
    id_website_domain   = models.ForeignKey('Website_domain', on_delete=models.CASCADE)


class Website_category(models.Model):
    id_category         = models.AutoField(primary_key=True)
    name_category       = models.CharField(max_length=50)


class Domain_category_website:
    id_category         = models.ForeignKey('Website_category', primary_key=True, on_delete=models.SET_NULL, null=True)
    id_website_domain   = models.ForeignKey('Website_domain', primary_key=True, on_delete=models.SET_NULL, null=True)


class Website_owner(models.Model):
    id_owner            = models.AutoField(primary_key=True)
    name                = models.CharField(max_length=50)
    type                = models.CharField(max_length=50)


class Search_history(models.Model):
    id_search_history   = models.AutoField(primary_key=True)
    user_id             = models.ForeignKey(User, on_delete=models.CASCADE)
    id_website_page     = models.ForeignKey('Website_page', on_delete=models.CASCADE)
    id_website_word     = models.ForeignKey('Website_word', on_delete=models.CASCADE)
    created_at          = models.DateTimeField(auto_now_add=True)