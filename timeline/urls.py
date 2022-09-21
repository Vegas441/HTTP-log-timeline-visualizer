from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    
urlpatterns = [
    path('', views.home, name='timeline-home'),
    path('log/<int:id>/', views.log, name='timeline-log'),
    path('timeline/<str:ip>', views.timeline, name='timeline-tm'),
    path('delete/', views.delete, name='delete')
]

urlpatterns += staticfiles_urlpatterns()

