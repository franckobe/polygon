from django.conf.urls import url
from polygonSearch import views

urlpatterns = [
    url(r'^login/', views.connexion, name='login'),
    url(r'^register/', views.register, name='register')
]
