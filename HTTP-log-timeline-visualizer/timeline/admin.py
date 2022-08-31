from sqlite3 import Time
from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Timeline)
admin.site.register(Log)
admin.site.register(Request)
admin.site.register(Data)