from django.shortcuts import render
from django.http import Http404
from rest_framework import permissions, status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import ProductSerializer, BasketItemSerializer
from .models import Product, BasketItem, Basket
from users.permisions import IsSellerPermission, IsOwnerOrReadOnly, IsOwnerOfBasket


def get_object(id, table):
    try:
        return table.objects.get(id=id)
    except table.DoesNotExist:
        raise Http404


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


class ProductDetailAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, id):
        product = get_object(id, Product)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductUpdateAPIView(APIView):
    permission_classes = [IsSellerPermission, IsOwnerOrReadOnly]

    def put(self, request, id):
        product = get_object(id, Product)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDeleteAPIView(APIView):
    permission_classes = [IsSellerPermission, IsOwnerOrReadOnly]

    def delete(self, request, id):
        product = get_object(id, Product)
        product.delete()
        return Response(status=status.HTTP_200_OK)


class BasketListAPIView(APIView):
    permission_classes = [IsOwnerOfBasket]

    def get(self, request):
        basket = Basket.objects.get(customer=request.user)
        basket_items = basket.items.all()
        serializer = BasketItemSerializer(basket_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BasketAddProductAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, id):
        basket = Basket.objects.get(customer=id)
        product_id = request.data.get('product_id')
        product = Product.objects.get(id=product_id)

        basket_item, created = BasketItem.objects.get_or_create(basket=basket, product=product)
        serializer = BasketItemSerializer(basket_item)
        if not created:
            basket_item.quantity += 1
            basket_item.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class BasketDetailAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, id):
        try:
            basket = Basket.objects.get(customer=id)
            basket_items = basket.items.all()
            serializer = BasketItemSerializer(basket_items, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Basket.DoesNotExist:
            return Response("Basket does not exist.", status=status.HTTP_404_NOT_FOUND)



