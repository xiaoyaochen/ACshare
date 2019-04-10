#-*-coding:utf-8-*-
'''
@project:ACshare
@author:释晓
@file:forms.py
@ide:PyCharm
@time:2019/4/9 下午 19:12
'''
from django import forms
from .models import Forums

class ForumsForm(forms.ModelForm):
    # def __init__(self,*args,**kwargs):
    #     this_user = kwargs.pop("user",None)
    #     super(ForumsForm, self).__init__()
    #     self.user = this_user

    # def save(self, commit=True):
    #     instance = super(ForumsForm, self).save()
    #     print(self.user)
    #     instance.author = self.user
    #     # print(instance.author)
    #     if commit:
    #         instance.save()
    #     return instance

    title = forms.CharField(required=False,
                            widget=forms.TextInput(attrs={"placeholder":"请输入内容"}))
    content = forms.CharField(min_length=5,max_length=350,
                              error_messages={
                                  "min_length":"最少不少于4个字符",
                                  "max_length":"最多不超过350个字符",
                                  "required":"内容不能为空"
                              },
                              widget=forms.Textarea(attrs={"placeholder":"请输入内容"}))


    class Meta:
        model = Forums
        fields = ['title','content']
