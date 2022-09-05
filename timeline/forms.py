from django import forms

class UploadFileFom(forms.Form):
    title = forms.CharField(max_length=100)
    file = forms.FileField()

class DateTimeForm(forms.Form):
    my_date_time_field: forms.DateTimeField()