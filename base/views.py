from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Room
from .forms import RoomForm

def home(request):
    rooms = Room.objects.all() # ModelName.objects => model manager to query from the database
    context = {'rooms':rooms}
    return render(request, 'base/home.html', context=context)

def room(request, id:str):
    room = Room.objects.get(id=id)
    context = {'room': room}
    return render(request, 'base/room.html', context=context)

def create_room(request):
    if request.method == "POST":
        form = RoomForm(request.POST) # form data is stored in request.POST along with csrf token
        if form.is_valid():
            form.save()
            return redirect('home') # using the name value of url
    form = RoomForm()
    context = {'form':form}
    return render(request, 'base/create-room.html', context=context)

def update_room(request, id):
    room = Room.objects.get(id = id)
    form = RoomForm(instance=room)
    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request, 'base/create-room.html', context=context)

def delete_room(request, id):
    room = Room.objects.get(id=id)

    if request.method == "POST":
        room.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj':room})