from django.conf.urls import url
from polygonSearch import views
from rest_framework.authtoken import views as apiViews

urlpatterns = [
    url(r'^login/$', views.login_view, name='login'),
    url(r'^login$', views.login_view, name='login'),
    url(r'^logout$', views.logout_view, name='logout'),
    url(r'^search$', views.search_view, name='search'),
    url(r'^register$', views.register_view, name='register'),
    url(r'^authenticate$', apiViews.obtain_auth_token),


    url(r'^search_result$', views.user_view, name='search_result'),

]
