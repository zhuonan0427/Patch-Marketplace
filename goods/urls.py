# goods/urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter

# 如果你有ViewSet,在这里注册
router = DefaultRouter()

urlpatterns = router.urls
