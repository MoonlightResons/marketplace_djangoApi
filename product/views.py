from django.shortcuts import render
from django.http import Http404
from rest_framework import permissions, status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import ProductSerializer
from .models import Product
from users.permisions import IsSellerPermission


class ProductCreateAPIView(APIView):
    permissions_classes = [IsSellerPermission]

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = Product.objects.create(
                name=request.data['name'],
                description=request.data['description'],
                price=request.data['price'],
                seller_id=request.data['seller']
            )
            product.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)


class ProductListAPIView(APIView):
    permissions_classes = [permissions.AllowAny]

    def get(self, request):
        product = Product.objects.all()
        serializer = ProductSerializer(product, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
