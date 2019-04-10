#-*-coding:utf-8-*-
'''
@project:Edu
@author:释晓
@file:sendEmail.py
@ide:PyCharm
@time:2019/3/5 下午 23:34
'''
from users.models import EmailVerification
from random import randrange
from django.core.mail import send_mail
from ACshare.settings import EMAIL_FROM

def get_code(lenth):
    choose = "1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
    code = ''
    for i in range(lenth):
        str = choose[randrange(0,len(choose))]
        code += str
    return code


def send_email(Email,send_type):
    code = get_code(8)
    a = EmailVerification()
    a.email = Email
    a.code = code
    a.send_type = send_type
    a.save()

    send_title = ''
    send_body = ''
    if send_type == 1:
        send_title = "欢迎注册ACshare动漫分享网:"
        send_body = '请点击以下链接进行激活您的账号：\nhttp://127.0.0.1:8000/users/user_active/'+code
        send_mail(send_title,send_body,EMAIL_FROM,[Email])
    elif send_type == 2:
        send_title = "ACshare重置密码系统:"
        send_body = '请点击以下链接进行激活您的账号：\nhttp://127.0.0.1:8000/users/user_reset/'+code
        send_mail(send_title,send_body,EMAIL_FROM,[Email])
