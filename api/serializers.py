from django.contrib.auth.models import User, Group
from rest_framework import serializers
from polygonSearch.models import Website_word, Website_page


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        exclude = []


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        exclude = []


class KeywordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Website_word
        exclude = []


class PageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Website_page
        exclude = []



