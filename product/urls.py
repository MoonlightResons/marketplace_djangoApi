from django.urls import path
from .views import (
    ProductCreateAPIView,
    ProductListAPIView,
    ProductDetailAPIView,
    ProductUpdateAPIView,
    ProductDeleteAPIView,
    BasketAddProductAPIView,
    BasketListAPIView,
    BasketDetailAPIView
)

urlpatterns = [
    path('create/', ProductCreateAPIView.as_view(), name='product-created'),
    path('list/', ProductListAPIView.as_view(), name='product-list'),
    path('<int:id>/', ProductDetailAPIView.as_view(), name='product-detail'),
    path('update/<int:id>/', ProductUpdateAPIView.as_view(), name='product-update'),
    path('<int:id>/delete/', ProductDeleteAPIView.as_view(), name='product-delete'),
    path('<int:id>/basket/add-product/', BasketAddProductAPIView.as_view(), name='basket-add'),
    path('basket/', BasketListAPIView.as_view(), name='basket-list'),
    path('<int:id>/basket-info/', BasketDetailAPIView.as_view(), name='basket-detail'),
]
