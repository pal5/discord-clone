from django.shortcuts import render
from django.http import HttpResponse

from .models import Room

def home(request):
    rooms = Room.objects.all() # ModelName.objects => model manager to query from the database
    context = {'rooms':rooms}
    return render(request, 'base/home.html', context=context)

def room(request, id:str):
    room = Room.objects.get(id=id)
    context = {'room': room}
    return render(request, 'base/room.html', context=context)

def create_room(request):
    context = {}
    return render(request, 'base/create-room.html', context=context)
