import os
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from django.core import serializers
from django.http import response, Http404, HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework import status
from .utils import get_tokens_for_user
from . import models
from . import apiserialize
from.models import User, Order, OrderItem, Product
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.authtoken.models import Token
import jwt
import stripe
import json
# Create your views here.
class Index(APIView):
    def get(self, request):
        queryset = models.Product.objects.all()
        serializer = apiserialize.ProductSerializer(queryset, many=True, context={"request":request})
        print(serializer)
        return Response(serializer.data)
    
class Search(APIView):
    def post(self, request):
        queryset = models.Product.objects.filter(product_name = request.data["search"].capitalize())
        serializer = apiserialize.ProductSerializer(queryset, many=True, context={"request":request})
        print(serializer.data)
        return Response(serializer.data)
    
class CreateUserAPI(APIView):
    # permission_classes = ("AllowAny",)
    # queryset = apiserialize.User.objects.get_or_create()
    # serializer_class = apiserialize.UserSeralizer

    def post(self, request):
        user = request.data
        serializer = apiserialize.UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.create(request.data)
        return Response(serializer.data, status= status.HTTP_201_CREATED)
    
class LoginView(APIView):
    def post(self, request):
        if 'email' not in request.data or 'password' not in request.data:
            return Response({'msg': 'Credentials missing'}, status=status.HTTP_400_BAD_REQUEST)
        email = request.data['email']
        password = request.data['password']
        user = authenticate(request, email=email, password=password)
        print(apiserialize.UserSerializer(user))
        if user is not None:
            login(request, user)
            auth_data = get_tokens_for_user(request.user)
            return Response({'msg': 'Login Success', **auth_data}, status=status.HTTP_200_OK)
        return Response({'msg': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'msg': 'Successfully Logged out'}, status=status.HTTP_200_OK)

class CurrentUserView(APIView):
    def get(self, request):
        token = request.headers["Cookie"].split(" ")[1]
        token_object = AccessToken(token)
        print(token_object)
        data = {'token': token}
        return Response(data)

class CreatePayment(APIView):
    def post(self, request):
        stripe.api_key= "sk_test_KF1bAynIegu7oJiu11KUOXF700dYVR8UAt"
        intent = stripe.PaymentIntent.create(
        amount= int(request.data["total"])*100,
        currency='USD',
        payment_method_types=["card"],
        metadata={'integration_check': 'accept_a_payment'},
        )
        data = {"CLIENT_SECRET": intent["client_secret"], "id":intent["id"]}
        return Response(data, status=status.HTTP_200_OK)

class CreateOrder(APIView):
    def post(self, request):
        data = request.data
        user_object_token = AccessToken(data["access"])
        print(data["access"])
        id = user_object_token["user_id"]
        user = User.objects.get(id=id)
        new_order = Order(user = user, order_total = request.data["cost"])
        new_order.save()

        for item in request.data["items"]:
            order_item = OrderItem(product = Product.objects.get(guid = item["product_id"]), cost = float(item["price"]), item_number=int(item["quantity"]), order = new_order)
            order_item.save()
        print(new_order.id)
        return Response({"order_id":new_order.id}, status=status.HTTP_200_OK)
    
class CheckPayment(APIView):
    def post(self, request):
        data = request.data
        data = stripe.PaymentIntent.retrieve(data["secret"])
        order = Order.objects.get(id=request.data["order_id"])
        if data["status"] == "succeeded":
            order.paid = True
            order.save()
        print(order.paid)
        return Response({"status": data["status"]}, status=status.HTTP_200_OK)

