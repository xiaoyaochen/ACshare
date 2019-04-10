#-*-coding:utf-8-*-
'''
@project:ACshare
@author:释晓
@file:urls.py
@ide:PyCharm
@time:2019/4/7 下午 23:06
'''
from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from .views import *


urlpatterns = [
    url(r'^forums_list',ForumsView,name='forums_list'),
    url(r'^forums_detail/(\d+)/$', Forums_detailView, name="forums_detail"),
    url(r'like/',like,name="like"),
    url(r'^forums_create',Forums_createView.as_view(),name="forums_create")
]
