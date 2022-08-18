from django.urls import path
from . import views
    
urlpatterns = [
    path('', views.home, name='timeline-home'),
    path('log/<int:id>/', views.log, name='timeline-log'),
    path('timeline/<str:ip>', views.timeline, name='timeline-tm')
]
