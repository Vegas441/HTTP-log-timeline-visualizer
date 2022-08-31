from django import forms

class UploadFileFom(forms.Form):
    title = forms.CharField(max_length=100)
    file = forms.FileField()