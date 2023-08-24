from django.urls import path
from .views import ProductCreateAPIView, ProductListAPIView


urlpatterns = [
    path('create/', ProductCreateAPIView.as_view(), name='product-created'),
    path('list/', ProductListAPIView.as_view(), name='product-list')
]