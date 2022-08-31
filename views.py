from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.conf.urls.static import static
from .models import *
from . import utils
from . import forms
from django.core.files.storage import FileSystemStorage

'''
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
'''

# Create your views here.
def home(request):
    context = {
        'timelines': Timeline.objects.all(),
        'logs': Log.objects.order_by('-dateTime').all(),
        'datas': Data.objects.all(),
        'requests': Request.objects.all()
    }
    try:
        if request.method == 'POST':
            uploaded_file = request.FILES['document']
            fs = FileSystemStorage()
            fs.save(uploaded_file.name, uploaded_file)
            #utils.read_file(uploaded_file.name)
            return render(request, 'timeline/home.html', context, utils.file_process('./media/' + uploaded_file.name))
        else:
            return render(request, 'timeline/home.html', context, utils.log_process())
    except:
        return render(request, 'timeline/connection_error.html')

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
    try:
        return render(request, 'timeline/log.html', context, utils.log_process())
    except:
        return render(request, 'timeline/connection_error.html')

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
    try:
        return render(request, 'timeline/timeline.html', context, utils.log_process())
    except:
        return render(request, 'timeline/connection_error.html')

def not_found_handler(request, exception):
    return render(request, 'timeline/404.html')