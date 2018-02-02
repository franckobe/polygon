from django.conf.urls import url
from crawlygon import views

urlpatterns = [
    url(r'^$', views.crawl),

]
