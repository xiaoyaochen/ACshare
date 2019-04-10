#-*-coding:utf-8-*-
'''
@project:ACshare
@author:释晓
@file:adminx.py
@ide:PyCharm
@time:2019/4/7 下午 21:27
'''

from .models import *
import xadmin

class ForumsXadmin(object):
    list_display = ['title','content','view_count','up_count','author','pub','priority']
    model_icon = "fa fa-credit-card "

# class ForumsCommentAadmin(object):
#     list_display = ['content','forums','user','add_time','parent_conment']
#     model_icon = "fa fa-commenting-o"


xadmin.site.register(Forums,ForumsXadmin)
# xadmin.site.register(ForumsComment,ForumsCommentAadmin)