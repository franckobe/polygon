from rest_framework import routers
from api import views

router = routers.SimpleRouter()
router.register(r'posts', views.PostViewSet)

urlpatterns = router.urls
