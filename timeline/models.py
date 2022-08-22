from django.db import models
from django.forms import IntegerField
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Timeline(models.Model):
    IP = models.CharField(max_length=45, primary_key=True)

class Log(models.Model):

    class type_T(models.TextChoices):
        SENT = 'SENT', _('SENT')
        RECIEVED = 'RECEIVED', _('RECEIVED')

    ID = models.IntegerField(primary_key=True)
    dateTime = models.DateTimeField()
    type = models.CharField(max_length=8, choices=type_T.choices) #SENT/RECEIVED
    restLogger = models.CharField(max_length=64)
    hostname = models.CharField(max_length=64)

    timeline = models.ForeignKey(Timeline, on_delete=models.CASCADE)

class Request(models.Model):

    class requestType_T(models.TextChoices):
        GET = 'GET', _('GET')
        POST = 'POST', _('POST')

    ID = models.IntegerField(primary_key=True)
    requestType = models.CharField(max_length=4, choices=requestType_T.choices) #GET/POST
    URL = models.CharField(max_length=256)
    params = models.CharField(max_length=64)

    log = models.ForeignKey(Log, on_delete=models.CASCADE)

class Data(models.Model):
    ID = models.IntegerField(primary_key=True)
    statusCode = models.IntegerField()
    hostname = models.CharField(max_length=64)
    ip = models.CharField(max_length=45)
    result = models.CharField(max_length=256)
    role = models.CharField(max_length=64)

    log = models.ForeignKey(Log, on_delete=models.CASCADE)

