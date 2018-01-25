from django.shortcuts import render
from crawlygon.models import PagesGetter

# Create your views here.


def crawl(request):
    pg = PagesGetter('http://www.nicolasremise.fr')
