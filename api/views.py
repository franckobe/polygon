from polygonSearch import models
from api import serializers
from rest_framework.viewsets import ReadOnlyModelViewSet


class PostViewSet(ReadOnlyModelViewSet):
    """
    A simple viewset to retrieve all the keyword
    """
    queryset = models.Website_word.objects.all().select_related('Website_word')
    serializer_class = serializers.WebsiteWordSerializer
