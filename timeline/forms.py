from sqlite3 import Date
from django import forms
from .widgets import DatePickerInput, TimePickerInput

class UploadFileFom(forms.Form):
    title = forms.CharField(max_length=100)
    file = forms.FileField()

class DateTimeForm(forms.Form):
    date = forms.DateField(widget=DatePickerInput)
    time = forms.TimeField(widget=TimePickerInput)