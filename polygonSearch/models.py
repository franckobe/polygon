from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=20)

    # ToDo set permission (1-2-3 / admin-user-superuser
    # editable = false, le champ sera exclus du form, pas la peine de le cacher
    typeUtil = models.IntegerField(editable=False)


