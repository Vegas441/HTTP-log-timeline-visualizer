from sqlite3 import Date
from django import forms
from .widgets import DatePickerInput, TimePickerInput
from .models import Log
import datetime

class UploadFileFom(forms.Form):
    title = forms.CharField(max_length=100)
    file = forms.FileField()

class DateTimeForm(forms.Form):

    date = forms.DateField(widget=DatePickerInput, initial=datetime.date.today)
    time = forms.TimeField(widget=TimePickerInput)

    # Add default date value from log 
    def_datetime = Log.objects.all().values('dateTime')
    def_datetime = def_datetime.first()['dateTime']
    print(def_datetime)
    if def_datetime:
        def_date = datetime.datetime.strftime(def_datetime, "%Y-%m-%d")
        date = forms.DateField(widget=DatePickerInput, initial=def_date)