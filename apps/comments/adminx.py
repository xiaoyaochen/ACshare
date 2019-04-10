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

class CommentXadmin(object):
    list_display = ['user','avatar','video','content','add_time']
    model_icon = "fa fa-caret-square-o-right"


xadmin.site.register(Comment,CommentXadmin)