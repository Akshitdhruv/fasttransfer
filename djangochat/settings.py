from decimal import ROUND_DOWN
from contextlib import contextmanager
from django.conf import settings
from py7zr import FILTER_DEFLATE,SevenZipFile
from time import sleep
from django.shortcuts import render, redirect
from more_itertools import sample
from pyppmd import compress
from pyzstd import compressionLevel_values
from torch import numel
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
import concurrent.futures
from pyunpack import Archive
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
number=0
r_size=0
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

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def createimg(req,s):
    global number
    name="samples"+str(number)
    number=number+1
    new_message = Message.objects.create(value=s[0], user=s[1], room=s[2],send_size=0,receive_size=0,ip_add="")
    global r_size
    msg=str(new_message.value.url)       
    me=msg.rfind("/")
    message=msg[me+1:len(msg)]
    ms="media/media/"+str(message)
    r_size=r_size+round(os.path.getsize(ms)/1024,2)
    dir="media/media/"
    oldpwd=os.getcwd()
    filters =[{'id': FILTER_DEFLATE}]
    archive = SevenZipFile("media/"+str(message)+".7z", mode='w', filters=filters)
    os.chdir(dir)
    archive.write(str(message))
    archive.close()
    os.chdir(oldpwd)
    dir="media/"
    os.chdir(dir)

    Message.objects.filter(value=new_message.value).delete()
    new_message = Message.objects.create(value=str(message)+".7z", user=s[1], room=s[2],send_size=0,receive_size=0,ip_add="")
    new_message.ip_add=get_client_ip(req)
    msg=str(new_message.value.url)        
    me=msg.rfind("/")
    message=msg[me+1:len(msg)]
    ms="media/"+str(message)
    size = round(os.path.getsize(ms)/1024,2)
    
    new_message.send_size=size 
    
    new_message.receive_size=round(r_size,2)    

    new_message.save()
    r_size=0
def remove(img):
    os.remove(img)



def send(request):
    if request.method=='POST':
        room = request.POST['room']
        username = request.POST['username']
        message = request.FILES['message'] 
        room_id = request.POST['room_id']
        try:
            for f in glob.iglob(os.path.join("media/media/", '*')):
                remove(f)
        except Exception:
            pass
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executors:   
            for i in request.FILES.getlist('message'):
                s=[i,username,room_id]
                createimg(request,s)
        
        
                
        
        """global number
        name="samples"+str(number)
        number=number+1
        shutil.make_archive("E:/8th_sem_project/django-chat-app/media/"+name, 'zip', "E:/8th_sem_project/django-chat-app/media/media/")
        new_message = Message.objects.create(value=name+".zip", user=username, room=room_id,size=0)
        msg=str(new_message.value.url)        
        me=msg.rfind("/")
        message=msg[me+1:len(msg)]
        ms="E:/8th_sem_project/django-chat-app/media/"+str(message)

        
        size = round(os.path.getsize(ms)/1024,2)
        print(size,"size")
        new_message.size=size
            
        new_message.save()"""
    context=Message.objects.all()
    return HttpResponseRedirect('/'+room+'/?username='+username,context)

      

def getMessages(request, room):
    room_details = Room.objects.get(name=room)
    
    messages = Message.objects.filter(room=room_details.id)
    msg=messages.values()
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executors: 
        for i in msg:
            x=i['value']
            z=x.rfind(".")
            
            if x[0:z] not in glob.iglob(os.path.join("E:/8th_sem_project/django-chat-app/media/media/", '*')):
                try:
                    archive = SevenZipFile('media/'+i['value'], mode='r')
                    x=i['value']
                    z=x.rfind(".")
                    archive.extractall(path="media/media/")
                    archive.close()
                    
                    i['value']='media/'+x[0:z]
                    
                except Exception:
                    pass
            else:
                x=i['value']
                z=x.rfind(".")
                i['value']='media/'+x[0:z]

        
    #archive = py7zr.SevenZipFile('E:/z.7z', mode='r')
    #archive.extractall(path="E:/output")
    #archive.close()
  
    #Archive(msg.value.url).extractall("E:/8th_sem_project/django-chat-app/media/temp")"""
    
    
    return JsonResponse({"messages":list(msg)})

