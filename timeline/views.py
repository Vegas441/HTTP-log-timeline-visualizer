from django.shortcuts import render
from django.http import HttpResponse
from django.conf.urls.static import static
from .models import *


example_ctx = {
    'time': '2022-07-04 07:14:29.523+01:00',
    'type': 'RECIEVED',
    'restLogger': '1139737886',
    'hostname': 'DEBUG master_1 RID1139737886',
    'status_code': '200',
    'ip': '10.1.0.14:5620',
    'result': '180',
    'role': 'SLAVE',
    'slave_hostname': 'slave_1'
}

# Create your views here.
def home(request):
    # Will be pulled from database
    context = {
        'timelines': Timeline.objects.all(),
        'logs': Log.objects.all(),
        'datas': Data.objects.all(),
        'requests': Request.objects.all()
    }
    return render(request, 'timeline/home.html', context)

def log(request, id):   #TODO: rozbehni 
    # Will be pulled from database
    context = {
        'log': Log.objects.filter(ID=id).first(),
        'requests': Request.objects.all(),
        'datas': Data.objects.all(),
    }
    return render(request, 'timeline/log.html', context)


def not_found_handler(request, exception):
    return render(request, 'timeline/404.html')