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
# This is an example context used in early phases of the project
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

def home(request):
    context = {
        'timelines': Timeline.objects.all(),
        'logs': Log.objects.order_by('-dateTime').all(),
        'datas': Data.objects.all(),
        'requests': Request.objects.all(),
        'filter_form': DateTimeForm()
    }
    try:
        # Load a fie
        if request.method == 'POST' and 'document' in request.FILES:
            uploaded_file = request.FILES['document']
            fs = FileSystemStorage()
            if fs.exists(uploaded_file.name):
                fs.delete(uploaded_file.name)
            fs.save(uploaded_file.name, uploaded_file)
            context = {
                'timelines': Timeline.objects.all(),
                'logs': Log.objects.order_by('-dateTime').all(),
                'datas': Data.objects.all(),
                'requests': Request.objects.all(),
                'filter_form': DateTimeForm()
            }
            return render(request, 'timeline/home.html', context, utils.file_process('./media/' + uploaded_file.name))
        
        # Load URL
        elif request.method == 'POST' and 'jenkins_url' in request.POST:
            url = request.POST['jenkins_url']
            context = {
                'timelines': Timeline.objects.all(),
                'logs': Log.objects.order_by('-dateTime').all(),
                'datas': Data.objects.all(),
                'requests': Request.objects.all(),
                'filter_form': DateTimeForm()
            }
            return render(request,'timeline/home.html', context) #TODO: funkcia na spracovanie dat z url

        # Filter by date and time 
        elif request.method == 'GET':
            form = DateTimeForm(request.GET)
            if form.is_valid():
                context['filter_form'] = form
                dateTimeLimit = datetime.combine(form.cleaned_data['date'], form.cleaned_data['time'])
                #print(dateTimeLimit)    
                context['logs'] = Log.objects.filter(dateTime__range = [dateTimeLimit, "9999-12-31 23:59:59"]).order_by('-dateTime')
            return render(request, 'timeline/home.html', context) #, utils.log_process())
            
        else:
            return render(request, 'timeline/home.html', context) #, utils.log_process())
    except Exception as e:
        print(e)
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
        return render(request, 'timeline/log.html', context)
    except:
        return render(request, 'timeline/connection_error.html')

def timeline(request, ip):
    timeline_ = Timeline.objects.filter(IP=ip).first()
    logs_ = Log.objects.filter(timeline=timeline_)
    requests_ = Request.objects.all()
    datas_ = Data.objects.all()
    
    # Filter by date and time 
    if request.method == 'GET':
        #print('get')
        form = DateTimeForm(request.GET)
        if form.is_valid():
            dateTimeLimit = datetime.combine(form.cleaned_data['date'], form.cleaned_data['time'])
            #print(dateTimeLimit)    
            logs_ = Log.objects.filter(timeline=timeline_, dateTime__range = [dateTimeLimit, "9999-12-31 23:59:59"])
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
        return render(request, 'timeline/timeline.html', context)
    except Exception as e:
        print(e)
        return render(request, 'timeline/connection_error.html')
    
# Delete all elements from database
def delete(request):
    timelines = Timeline.objects.all()
    timelines.delete()     
    return render(request,'timeline/home.html')

def not_found_handler(request, exception):
    return render(request, 'timeline/404.html')