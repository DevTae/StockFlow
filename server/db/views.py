from django.shortcuts import render
from django.http import HttpResponse

from .models import theme_type

def index(request):
    return HttpResponse("Hello, world.")

def insert_test():
    new_theme_type = theme_type()
    new_theme_type.theme_name = "name"
    new_theme_type.theme_description = "contents"
    new_theme_type.save()

def update_test():
    selected = theme_type.objects.get(sector_id=1)
    selected.theme_description = "test"
    selected.save()
