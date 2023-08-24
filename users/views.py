import jwt
from django.http import Http404
from django.shortcuts import render
from django.contrib.auth import login
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework_simplejwt import exceptions
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import permissions, status
from .serializers import SellerSerializer, CustomerSerializer, MyTokenObtainPairSerializer
from .models import Seller, Customer
from .permisions import AnnonPermission


class LoginView(TokenObtainPairView):
    permission_classes = (AnnonPermission,)
    serializer_class = MyTokenObtainPairSerializer


class SellerRegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = SellerSerializer(data=request.data)
        if serializer.is_valid():
            seller = Seller.objects.create(
                email=request.data['email'],
                is_Seller=True,
                name=request.data['name'],
                second_name=request.data['second_name'],
                phone_number=request.data['phone_number'],
                description=request.data['description']
            )
            seller.set_password(request.data['password'])
            seller.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SellerLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        seller = authenticate(request, email=email, password=password)

        if seller:
            refresh = RefreshToken.for_user(seller)
            serializer = MyTokenObtainPairSerializer(data={
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
            serializer.is_valid()
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class CustomerRegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            customer = Customer.objects.create(
                email=request.data['email'],
                name=request.data['name'],
                second_name=request.data['second_name'],
                phone_number=request.data['phone_number'],
                card_number=request.data['card_number'],
                post_code=request.data['post_code']
            )
            customer.set_password(request.data['password'])
            customer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        customer = authenticate(request, email=email, password=password)

        if customer:
            refresh = RefreshToken.for_user(customer)
            serializer = MyTokenObtainPairSerializer(data={
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
            serializer.is_valid()
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class SellerListAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        product = Seller.objects.all()
        serializer = SellerSerializer(product, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CustomerListAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        product = Customer.objects.all()
        serializer = CustomerSerializer(product, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)