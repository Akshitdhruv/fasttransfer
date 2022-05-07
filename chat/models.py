from django.db import models
from datetime import datetime

# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=1000)
class Message(models.Model):
    value = models.FileField(upload_to="media",null=True, blank=True)
    date = models.DateTimeField(default=datetime.now, blank=True)
    user = models.CharField(max_length=1000000)
    room = models.CharField(max_length=1000000)
    size = models.CharField(default=0,max_length=1000000)
