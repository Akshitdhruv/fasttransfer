from decimal import ROUND_DOWN
from django.shortcuts import render, redirect
from more_itertools import sample
from chat.models import Room, Message
from django.http import HttpResponse, JsonResponse
from datetime import datetime
from .models import Message
from io import BytesIO
from django.http import HttpResponseRedirect
from django.core import files
import os
from zipfile import ZipFile
from PIL import Image
import shutil
import glob, os,os.path
# Create your views here.
def home(request):
    return render(request, 'home.html')

def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'room.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })


def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']



    if Room.objects.filter(name=room).exists():
        return redirect('/'+room+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/'+room+'/?username='+username)

    return render(request,'index1.html',{'context':context})
def send(request):
    if request.method=='POST':
        room = request.POST['room']
        username = request.POST['username']
        
        message = request.FILES['message']
       
            
        room_id = request.POST['room_id']
        for i in request.FILES.getlist('message'):
            new_message = Message.objects.create(value=i, user=username, room=room_id,size=0)
            """msg=str(new_message.value.url)        
            me=msg.rfind("/")
            message=msg[me+1:len(msg)]
            ms="E:/8th_sem_project/django-chat-app/media/media/"+str(message)"""
        shutil.make_archive("E:/8th_sem_project/django-chat-app/media/sampless", 'zip', "E:/8th_sem_project/django-chat-app/media/media/")
        
    
        new_message = Message.objects.create(value="sampless.zip", user=username, room=room_id,size=0)
        msg=str(new_message.value.url)        
        me=msg.rfind("/")
        message=msg[me+1:len(msg)]
        ms="E:/8th_sem_project/django-chat-app/media/"+str(message)

       
        size = round(os.path.getsize(ms)/1024,2)
        print(size,"size")
        new_message.size=size
        
        new_message.save() 
        for f in glob.iglob(os.path.join("E:/8th_sem_project/django-chat-app/media/media/", '*')):
            os.remove(f)
        
    context=Message.objects.all()
    return HttpResponseRedirect('/'+room+'/?username='+username,context)

      

def getMessages(request, room):
    room_details = Room.objects.get(name=room)
    
    messages = Message.objects.filter(room=room_details.id)
    msg=messages.values()
    
    return JsonResponse({"messages":list(messages.values())})

