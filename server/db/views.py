from django.shortcuts import render
from django.http import HttpResponse

from .models import theme_type

def index(request):
    return HttpResponse("Hello, world.")
