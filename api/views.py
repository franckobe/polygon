from polygonSearch import models
from api import serializers
from rest_framework.viewsets import ReadOnlyModelViewSet


class PostViewSet(ReadOnlyModelViewSet):
    """
    A simple viewset to retrieve all the keyword
    """
    queryset = models.Post.objects.all.selected_relateted('Website_page')
    serializer_class = serializers.PostSerializer
