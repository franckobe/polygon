from rest_framework import serializers
from polygonSearch import models

class WebsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        field = ('id_website_page', 'url', 'title', 'content', 'id_website_domain')


class PostSerializer(serializers.ModelSerializer):
    websiteSerializer = WebsiteSerializer()

    # Les serializers vont nous permettre de serialiser les instances en JSON et transformer le JSON en instance python.
    class Meta:
        model = models.Post
        field = ('id_website_word', 'word', 'weight', 'url', 'id_website_page')
        depth = 1
