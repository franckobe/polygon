from django.conf.urls import url
from crawlygon import views

urlpatterns = [
    url(r'^$', views.crawl_view, name='crawl_view'),
    url(r'^crawl$', views.crawl, name='crawl'),
    url(r'^crawl-links$', views.crawl_links, name='crawl_links'),

]
