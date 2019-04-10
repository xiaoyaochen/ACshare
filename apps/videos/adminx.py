#-*-coding:utf-8-*-
'''
@project:ACshare
@author:释晓
@file:adminx.py
@ide:PyCharm
@time:2019/3/18 下午 21:17
'''
from .models import *
import xadmin

class ClassificationXadmin(object):
    list_display = ['title','status']
    model_icon = "fa fa-caret-square-o-right"

class VideoInfoXadmin(object):
    list_display = ['title','desc','classification','file','cover','status','view_count','collected','liked','up_man','add_time']
    model_icon = "fa fa-link"


xadmin.site.register(Classification,ClassificationXadmin)
xadmin.site.register(VideoInfo,VideoInfoXadmin)
