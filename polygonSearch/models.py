from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class User(models.Model):
    id_user = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50).blank = False
    password = models.CharField(max_length=20).blank = False
    email = models.EmailField.blank = True
    picture = models.ImageField.blank = True
    #ToDo add date.now() à la création
    date_create = models.DateField.blank = False
    #ToDo add date.now() à la création
    date_update = models.DateField.blank = True
    date_birthday = models.DateField.blank = True

    # ToDo set permission (1-2-3 / admin-user-superuser
    # editable = false, le champ sera exclus du form, pas la peine de le cacher
    typeUtil = models.IntegerField(editable=False)


