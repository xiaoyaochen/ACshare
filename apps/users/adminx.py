#-*-coding:utf-8-*-
'''
@project:ACshare
@author:释晓
@file:adminx.py
@ide:PyCharm
@time:2019/3/25 上午 11:57
'''
import xadmin
from .models import BannerInfo,EmailVerification,Feedback
from xadmin import views
class BaseXadminSetting(object):
    enable_themes = True
    use_bootswatch = True

class CommXadminSetting(object):
    site_title = 'ACshare动漫分享平台系统'
    site_footer = 'ACshard动漫分享平台'
    menu_style = 'accordion'

class BannerInfoXadmin(object):
    list_display = ['image','url','add_time']
    search_fields = ['image','url']
    list_filter = ['image','url']

class EmailVerificationXadmin(object):
    list_display = ['code','email','send_type','add_time']

class FeedbackXadmin(object):
    list_diaplay = ['contact','content','timestamp']


xadmin.site.register(BannerInfo,BannerInfoXadmin)
xadmin.site.register(EmailVerification,EmailVerificationXadmin)
xadmin.site.register(Feedback,FeedbackXadmin)
xadmin.site.register(views.BaseAdminView,BaseXadminSetting)
xadmin.site.register(views.CommAdminView,CommXadminSetting)