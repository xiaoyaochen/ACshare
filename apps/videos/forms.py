#-*-coding:utf-8-*-
'''
@project:ACshare
@author:释晓
@file:forms.py
@ide:PyCharm
@time:2019/3/18 上午 11:47
'''
from django import forms
from comments.models import Comment
from videos.models import VideoInfo,Classification
from users.models import UserProfile

class CommentForm(forms.ModelForm):
    content = forms.CharField(error_messages={'required':'不能为空',},
                              widget=forms.Textarea(attrs={'placeholder':'请输入评论内容'}))

    class Meta:
        model = Comment
        fields = ['content']

class VideoPublishForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        this_user = kwargs.pop('user',None)
        super(VideoPublishForm, self).__init__(*args,**kwargs)
        self.user = this_user
        # self.fields['up_man'].queryset = UserProfile.objects.get(username=self.user)
        # print(self.fields['up_man'])

    def save(self, commit=True):
        instance = super(VideoPublishForm, self).save()
        instance.up_man = self.user
        if commit:
            instance.save()
        return instance
    title = forms.CharField(min_length=4,max_length=200,required=True,
                            error_messages={
                                'min_length':'至少4个字符',
                                'max_length':'不能多于200个字符',
                                'required':'标题不能为空'
                            },
                            widget=forms.TextInput(attrs={'placeholder':'请输入内容'}))

    desc = forms.CharField(min_length=4, max_length=200, required=True,
                           error_messages={
                               'min_length': '至少4个字符',
                               'max_length': '不能多于200个字符',
                               'required': '描述不能为空'
                           },
                           widget=forms.Textarea(attrs={'placeholder': '请输入内容'}))
    cover = forms.ImageField(required=True,
                             error_messages={
                                 'required': '封面不能为空'
                             },
                             widget=forms.FileInput(attrs={'class': 'n'}))
    status = forms.CharField(min_length=1, max_length=1, required=False,
                             widget=forms.HiddenInput(attrs={'value': '0'}))


    class Meta:
        model = VideoInfo
        fields = ['title', 'desc', 'status', 'cover', 'classification']


class VideoEditForm(forms.ModelForm):
    title = forms.CharField(min_length=4, max_length=200, required=True,
                            error_messages={
                                'min_length': '至少4个字符',
                                'max_length': '不能多于200个字符',
                                'required': '标题不能为空'
                            },
                            widget=forms.TextInput(attrs={'placeholder': '请输入内容'}))
    desc = forms.CharField(min_length=4, max_length=200, required=True,
                           error_messages={
                               'min_length': '至少4个字符',
                               'max_length': '不能多于200个字符',
                               'required': '描述不能为空'
                           },
                           widget=forms.Textarea(attrs={'placeholder': '请输入内容'}))
    cover = forms.ImageField(required=True,
                             error_messages={
                                 'required': '封面不能为空'
                             },
                             widget=forms.FileInput(attrs={'class': 'n'}))

    status = forms.CharField(min_length=1, max_length=1, required=False,
                             widget=forms.HiddenInput())


    class Meta:
        model = VideoInfo
        fields = ['title', 'desc', 'status', 'cover','classification']
