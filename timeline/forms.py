from django import forms
from .widgets import DateTimePickerInput

class UploadFileFom(forms.Form):
    title = forms.CharField(max_length=100)
    file = forms.FileField()

class DateTimeForm(forms.Form):
    Select_date_and_time = forms.DateTimeField() #TODO pridaj widget 