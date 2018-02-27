from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from crawlygon.models import PagesGetter, CrawlerInstructor


@login_required(login_url='/polygonSearch/login')
def crawl_view(request):
    return render(request, "crawler.html")


@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
@api_view(['POST'])
def crawl(request):
    if request.method == "POST":
        url = request.POST.get("url")
        if url is not None and not url == "":
            pg = PagesGetter(url=url)
    return Response()


@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
@api_view(['POST'])
def crawl_links(request):
    if request.method == "POST":
        iteration = request.POST.get("iteration")
        if iteration is not None and not iteration == "":
            pg = CrawlerInstructor(nbIterations=iteration)
        else:
            pg = CrawlerInstructor()
    return Response()
