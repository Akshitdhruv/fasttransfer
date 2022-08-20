from django.db import models
from datetime import datetime

class Room(models.Model):
    name = models.CharField(max_length=1000)
class Message(models.Model):
    value = models.FileField(upload_to="media",null=True, blank=True)
    date = models.DateTimeField(default=datetime.now, blank=True)
    user = models.CharField(max_length=1000000)
    room = models.CharField(max_length=1000000)
    send_size = models.CharField(default=0,max_length=1000000)
    receive_size = models.CharField(default=0,max_length=1000000)
    ip_add= models.CharField(default=0,max_length=1000000)
