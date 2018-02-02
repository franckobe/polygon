from django.contrib.auth.models import User, Group
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.permissions import IsOwnerOrReadOnly
from api import serializers
from api.serializers import KeywordSerializer
from polygonSearch.models import Website_page, Website_word


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
def word(request, word=None):
    if request.method == 'GET':
        result = Website_word.objects.get(word=word)
        serializer = KeywordSerializer(result, many=False)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        result = Website_word.objects.get(word=word)
        result.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
