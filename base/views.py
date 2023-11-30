from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from .models import Room, Topic, Message
from .forms import RoomForm

def login_page(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("password")
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User Does Not Exist.")
            return render(request, 'base/login-register.html', {})

        user = authenticate(request, username=user, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password is incorrect')
    context = {'page':page}
    return render(request, 'base/login-register.html', context)

def sign_up(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, "Error occured during registration")
    context = {'form':form}
    return render(request, 'base/login-register.html', context)

def logout_page(request):
    logout(request)
    return redirect('home')

def home(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ""
    rooms = Room.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q)) # ModelName.objects => model manager to query from the database
    topics = Topic.objects.all()
    rooms_count = rooms.count()
    context = {'rooms':rooms,'topics':topics,'rooms_count':rooms_count}
    return render(request, 'base/home.html', context=context)

def room(request, id:str):
    room = Room.objects.get(id=id)
    if request.method == "POST":
        message = Message.objects.create(user=request.user, body=request.POST.get('body'), room=room )
        room.participants.add(request.user)
        return redirect('room', id=room.id)
    participants = room.participants.all()
    room_messages = room.message_set.all().order_by('-created') # using parent room object you can access all children object ( in one:many mapping )
    context = {'room': room, 'room_messages':room_messages, 'participants': participants}
    return render(request, 'base/room.html', context=context)

@login_required(login_url='login')
def create_room(request):
    if request.method == "POST":
        form = RoomForm(request.POST) # form data is stored in request.POST along with csrf token
        if form.is_valid():
            form.save()
            return redirect('home') # using the name value of url
    form = RoomForm()
    context = {'form':form}
    return render(request, 'base/create-room.html', context=context)

@login_required(login_url='login')
def update_room(request, id):
    room = Room.objects.get(id = id)

    if request.user != room.host:
        return HttpResponse("You don't own this room to update")
    
    form = RoomForm(instance=room)
    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request, 'base/create-room.html', context=context)

@login_required(login_url='login')
def delete_room(request, id):
    room = Room.objects.get(id=id)

    if request.user != room.host:
        return HttpResponse("You don't own this room to delete")
    
    if request.method == "POST":
        room.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj':room})