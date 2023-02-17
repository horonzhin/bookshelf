from django.urls import include, path
from rest_framework import routers

from api import views

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'books', views.BookModelViewSet)
router.register(r'baskets', views.BasketModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
