from rest_framework import serializers
from polygonSearch import models

class WebsitePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Website_page
        fields = "__all__"


class WebsiteWordSerializer(serializers.ModelSerializer):
    websiteSerializer = WebsitePageSerializer()

    # Les serializers vont nous permettre de serialiser les instances en JSON et transformer le JSON en instance python.
    class Meta:
        model = models.Website_word
        fields = "__all__"
        depth = 1
