"""djangoProject1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

app_name = 'upload'
urlpatterns = [
    path('',views.index),
    path('exploit/',views.exploit),
    path('file/',views.userfile,name='userfile'),
    path('file/detail/',views.detailFile,name='delfile'),
    path('meetings/',views.meetings,name='meetings'),
    path('meetings/meetingdetailPage',views.meetingdetailPage,name='meetingdetailPage'),
    path('meetings/meetingdetail',views.meetingdetail,name='meetingdetail'),
    path('meetings/meetingdetailtest',views.meetingdetailtest,name='meetingdetailtest'),
    path('downloadfile/',views.downloadfile,name='downloadfile'),
]
