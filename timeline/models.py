from django.db import models
from django.forms import IntegerField
#from django.utils import timezone

# Create your models here.

class Timeline(models.Model):
    IP = models.CharField(max_length=45, primary_key=True)

class Log(models.Model):
    ID = models.IntegerField(primary_key=True)
    dateTime = models.DateTimeField()
    type = models.CharField(max_length=8) #SENT/RECIEVED
    restLogger = models.CharField(max_length=64)
    hostname = models.CharField(max_length=64)

    timeline = models.ForeignKey(Timeline, on_delete=models.CASCADE)

class Request(models.Model):
    ID = models.IntegerField(primary_key=True)
    requestType = models.CharField(max_length=4) #GET/POST
    params = models.CharField(max_length=64)
    URL = models.CharField(max_length=256)

    log = models.ForeignKey(Log, on_delete=models.CASCADE)

class Data(models.Model):
    ID = models.IntegerField(primary_key=True)
    statusCode = models.IntegerField()
    hostname = models.CharField(max_length=64)
    ip = models.CharField(max_length=45)
    result = models.CharField(max_length=256)
    role = models.CharField(max_length=64)

    log = models.ForeignKey(Log, on_delete=models.CASCADE)

