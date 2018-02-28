from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework.test import APIRequestFactory
from polygonSearch.models import Website_word, Website_page
from rest_framework.request import Request


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = []


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        exclude = []


class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Website_word
        exclude = []


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Website_page
        exclude = []



