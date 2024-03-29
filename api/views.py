from django.contrib.auth.models import User, Group
from math import ceil
from rest_framework import viewsets, status, permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from api.permissions import IsOwnerOrReadOnly
from api import serializers
from api.serializers import KeywordSerializer, PageSerializer
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from polygonSearch.models import Website_page, Website_word, Search_history


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = serializers.UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer


@api_view(['GET', 'POST'])
def word_list(request, sort=None, desc=None):
    """ get all the key words by sorting
    :param object request:
    :param str sort: field to sort
    :param boolean desc: if descending
    return the word list sorted or not"""
    if request.method == 'GET':
        wordList = Website_word.objects.all()
        if sort:
            if desc:
                wordList = wordList.sort('-' + sort)
            else:
                wordList = wordList.sort(sort)
        serializer = KeywordSerializer(wordList, many=True)
        return Response(serializer.data)


@api_view(['GET', 'DELETE'])
def word(request, word):
    if request.method == 'GET':
        result = Website_word.objects.all().filter(word=word)
        serializer = KeywordSerializer(result, many=True)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        result = Website_word.objects.get(word=word)
        result.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def page(request, word):
    if request.method == 'GET':
        tempResult = Website_word.objects.get(word=word)
        tempSerializer = KeywordSerializer(tempResult, many=False)
        result = Website_page.objects.get(id_website_page=tempSerializer.data['id_website_page'])
        serializer = PageSerializer(result, many=False)
        return Response(serializer.data)


@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes(IsAuthenticated)
@api_view(['GET'])
def results(request):
    word = request.GET.get('q')
    nb = int(request.GET.get('nb') if not None else 10)
    p = int(request.GET.get('p') if not None else 0)
    offset = (p - 1) * nb
    pages = []
    nbwords = int(Website_word.objects.filter(word__contains=word).count())
    nbp = ceil(nbwords/nb)
    words = Website_word.objects.filter(word__contains=word).order_by('-weight')[offset:nb+offset]
    for wd in words:
        pid = wd.id_website_page.id_website_page
        result = Website_page.objects.get(id_website_page=pid)
        ps = PageSerializer(result)
        pages.append(ps.data)
    search_results = {
        'nb': nbwords,
        'nbp': nbp,
        'curp': p,
        'results': pages
    }
    if not request.GET.get('history') is None and p == 1:
        search_history = Search_history(user=request.user, word=word, nb_results=nbwords)
        search_history.save()
    return Response(search_results)
