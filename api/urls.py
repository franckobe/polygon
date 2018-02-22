from django.conf.urls import url, include
from rest_framework.authtoken import views as apiViews
from . import views


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^word$', views.word_list),
    url(r'^word/(?P<word>[A-z]+)$', views.word),

    # authentication
    url(r'^authenticate$', apiViews.obtain_auth_token),
    url(r'^api-auth/', include('rest_framework.urls')),
]
