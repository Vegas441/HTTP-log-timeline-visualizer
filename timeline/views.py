from django.shortcuts import render
from django.http import HttpResponse
from django.conf.urls.static import static
from .models import *
<<<<<<< HEAD
from . import utils 
=======
from . import utils
>>>>>>> d48a83aee1a51e9692027ead631e266c1a786702


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
    context = {
        'timelines': Timeline.objects.all(),
        'logs': Log.objects.all(),
        'datas': Data.objects.all(),
        'requests': Request.objects.all()
    }
    return render(request, 'timeline/home.html', context, utils.log_process())

def log(request, id):   
    # Will be pulled from database
    log_ = Log.objects.filter(ID=id).first()
    request_ = Request.objects.filter(log = log_).first()
    data_ = Data.objects.filter(log=log_).first()
    context = {
        'log': log_,
        'request': request_,
        'data': data_
    }
    return render(request, 'timeline/log.html', context, utils.log_process())

def timeline(request, ip):
    timeline_ = Timeline.objects.filter(IP=ip).first()
    logs_ = Log.objects.filter(timeline=timeline_)
    requests_ = Request.objects.all()
    datas_ = Data.objects.all()

    context = {
        'timeline': timeline_,
        'logs': logs_,
        'requests': requests_,
        'datas': datas_
    }
    return render(request, 'timeline/timeline.html', context, utils.log_process())

def not_found_handler(request, exception):
    return render(request, 'timeline/404.html')