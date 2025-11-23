from django.urls import path
from . import views

urlpatterns = [
    path('goods/', views.goods_list),
    path('goods/<int:id>/', views.goods_detail)
]