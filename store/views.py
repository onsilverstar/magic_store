from django.shortcuts import render
from django.http import response, Http404, HttpResponse
from . import models

# Create your views here.
def index(request):
    return HttpResponse(request, "Hi")
