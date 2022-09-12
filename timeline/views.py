from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.conf.urls.static import static
from .models import *
from . import utils
from . import forms
from django.core.files.storage import FileSystemStorage
from .forms import DateTimeForm
from datetime import datetime, tzinfo, timezone

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
            if fs.exists(uploaded_file.name):
                fs.delete(uploaded_file.name)
            fs.save(uploaded_file.name, uploaded_file)
            utils.file_process('./media/' + uploaded_file.name)
            context = {
                'timelines': Timeline.objects.all(),
                'logs': Log.objects.order_by('-dateTime').all(),
                'datas': Data.objects.all(),
                'requests': Request.objects.all()
            }
            return render(request, 'timeline/home.html', context, utils.file_process('./media/' + uploaded_file.name))
        else:
            return render(request, 'timeline/home.html', context, utils.log_process())
    except:
        return render(request, 'timeline/connection_error.html')

def home_file(request):
    context = {
        'timelines': Timeline.objects.all(),
        'logs': Log.objects.order_by('-dateTime').all(),
        'datas': Data.objects.all(),
        'requests': Request.objects.all()
    }
    if request.method == 'POST':
        try:
            uploaded_file = request.FILES['document']
            fs = FileSystemStorage()
            fs.save(uploaded_file.name, uploaded_file)
            utils.read_file(uploaded_file.name)
            return render(request, 'timeline/home.html', context, utils.file_process('./media/' + uploaded_file.name))
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
    
    if request.method == 'GET':
        print('get')
        form = DateTimeForm(request.GET)
        if form.is_valid():
            dateTimeLimit = datetime.combine(form.cleaned_data['date'], form.cleaned_data['time'])
            #dateTimeLimit = dateTimeLimit.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            #dateTimeLimit = datetime(2022, 7, 1, 12, 30, 00, 000000, tzinfo=timezone.utc)
            print(dateTimeLimit)    
            logs_ = Log.objects.filter(timeline=timeline_, dateTime = dateTimeLimit)
        #TODO oprav
        else: 
            form = DateTimeForm()

    context = {
        'timeline': timeline_,
        'logs': logs_,
        'requests': requests_,
        'datas': datas_,
        'form': form
    }  

    try:
        return render(request, 'timeline/timeline.html', context, utils.log_process())
    except Exception as e:
        print(e)
        return render(request, 'timeline/connection_error.html')

def not_found_handler(request, exception):
    return render(request, 'timeline/404.html')