from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

rooms = [
    {'id':1, 'name': "Learning BufferOverFlow"},
    {'id':2, 'name': "Front End Dev"},
    {'id':3, 'name': "Self Help Group"},
]

def home(request):
    context = {'rooms':rooms}
    return render(request, 'home.html', context=context)

def room(request):
    return render(request, 'room.html')
