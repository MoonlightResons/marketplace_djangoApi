from django.urls import path, include
from .views import CustomerRegisterView, SellerRegisterView, SellerLoginView, CustomerLoginView, CustomerListAPIView, SellerListAPIView

urlpatterns = [
    path('register/seller/', SellerRegisterView.as_view(), name='seller-register'),
    path('register/customer/', CustomerRegisterView.as_view(), name='customer-register'),
    path('login/seller/', SellerLoginView.as_view(), name='seller-login'),
    path('login/customer/', CustomerLoginView.as_view(), name='customer-login'),
    path('seller/list/', SellerListAPIView.as_view(), name='seller-list'),
    path('customer/list/', CustomerListAPIView.as_view(), name='customer-list'),
]