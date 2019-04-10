#-*-coding:utf-8-*-
'''
@project:Edu
@author:释晓
@file:forms.py
@ide:PyCharm
@time:2019/3/5 下午 16:11
'''
from django import forms
from captcha.fields import CaptchaField
from django.contrib.auth.forms import UserChangeForm,AuthenticationForm,PasswordChangeForm
from django.core.exceptions import ValidationError
from .models import UserProfile,Feedback

def avatar_file_size(value):
    limit = 2*1024*1024
    if value.size >limit:
        raise ValidationError('头像文件太大了，请限制在2M之内')

class ProfileForm(forms.ModelForm):
    nick_name = forms.CharField(min_length=1,max_length=20,required=False,
                                error_messages={
                                    'min_length':'昵称至少4个字符',
                                    'max_length':'昵称不能够多于20个字符'
                                },
                                widget=forms.TextInput())
    avatar = forms.ImageField(required=False, validators=[avatar_file_size],
                              widget=forms.FileInput(attrs={'class': 'n'}))
    email = forms.EmailField(required=False,
                             error_messages={
                                 'invalid': '请输入有效的Email地址',
                             },
                             widget=forms.EmailInput())
    gender = forms.CharField(min_length=1, max_length=1, required=False,
                             widget=forms.HiddenInput())

    phone = forms.CharField(min_length=11, max_length=11, required=False,
                             error_messages={
                                 'min_length': '请输入11位手机号',
                                 'max_length': '请输入11位手机号',
                             },
                             widget=forms.NumberInput())

    class Meta:
        model = UserProfile
        fields = ['nick_name', 'avatar', 'email', 'gender', 'phone']

class ChangeePwdForm(PasswordChangeForm):
    old_password = forms.CharField(error_messages={'required':'不能为空',},
                                   widget=forms.PasswordInput(attrs={'placeholder':'请输入旧密码'}))
    new_password1 = forms.CharField(error_messages={'required': '不能为空', },
                                    widget=forms.PasswordInput(attrs={'placeholder': '请输入新密码'})
                                    )
    new_password2 = forms.CharField(error_messages={'required': '不能为空', },
                                    widget=forms.PasswordInput(attrs={'placeholder': '请输入确认密码'})
                                    )


class SubscribeForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['subscribe']


class FeedbackForm(forms.ModelForm):
    content = forms.CharField(min_length=4,max_length=200,
                              error_messages={
                                  'min_length': '至少4个字符',
                                  'max_length': '不能多于200个字符',
                                  'required': '内容不能为空'
                              },
                              widget=forms.Textarea(attrs={'placeholder':'请输入内容'}))
    contact = forms.CharField(required=False,
                              widget=forms.TextInput(attrs={'placeholder': '请输入联系方式'}))
    class Meta:
        model = Feedback
        fields = ['content', 'contact']


class UserRegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True,min_length=6,error_messages={
        "required":"密码必须填写！",
        "min_length":"密码不能短于6位！",
    })
    captcha = CaptchaField()


class UserLoginForm(forms.Form):
    username = forms.EmailField(required=True)
    password = forms.CharField(required=True,min_length=6,error_messages={
        "required":"密码必须填写！",
        "min_length":"密码不能短于6位！",
    })
    captcha = CaptchaField()

class UserForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField()



class UserResetForm(forms.Form):
    password1 = forms.CharField(required=True,min_length=6,error_messages={
        "required":"密码必须填写！",
        "min_length":"密码不能短于6位！",
    })
    password2 = forms.CharField(required=True, min_length=6, error_messages={
        "required": "密码必须填写！",
        "min_length": "密码不能短于6位！",
    })

