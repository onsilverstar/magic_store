from django.shortcuts import render
# from rest_framework import viewsets
from rest_framework.views import APIView
from django.core import serializers
from django.http import response, Http404, HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework import status
from . import models
from . import apiserialize

# Create your views here.
def index(request):
    all_products = list(models.Product.objects.all())
    all_products = serializers.serialize("json", all_products)
    return HttpResponse(all_products, content_type="application/json")

class CreateUserAPI(APIView):
    # permission_classes = ("AllowAny",)
    # queryset = apiserialize.User.objects.get_or_create()
    # serializer_class = apiserialize.UserSeralizer

    def post(self, request):
        user = request.data
        serializer = apiserialize.UserSeralizer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status= status.HTTP_201_CREATED)
