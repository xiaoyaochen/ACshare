from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
# Create your models here.

class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=20,verbose_name="用户昵称",blank=True,null=True)
    avatar = models.FileField(upload_to="users/%y/%m/%d",verbose_name="用户头像")
    birthday = models.DateTimeField(verbose_name="用户生日",null=True,blank=True)
    gender = models.CharField(max_length=1,choices=(('M','男'),('F','女')),verbose_name="用户性别",blank=True, null=True)
    phone = models.CharField(max_length=11,verbose_name="用户手机")
    is_start = models.BooleanField(default=False,verbose_name='是否激活')
    up_count = models.IntegerField(default=0,verbose_name="上传数量")
    subscribe = models.BooleanField(default=False)
    add_time = models.DateTimeField(default=datetime.now,verbose_name="添加时间")

    def __str__(self):
        return self.username
    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name


class BannerInfo(models.Model):
    image = models.ImageField(upload_to='banners/%y/%m/%d',max_length=200,verbose_name='轮播图片')
    url = models.URLField(max_length=200,verbose_name="轮播链接")
    add_time = models.DateTimeField(default=datetime.now,verbose_name="添加时间")

    def __str__(self):
        return str(self.image)

    class Meta:
        verbose_name = "轮播图信息"
        verbose_name_plural = verbose_name

class EmailVerification(models.Model):
    email = models.EmailField(max_length=50,verbose_name="邮箱")
    code = models.CharField(max_length=20,verbose_name="验证码")
    send_type = models.CharField(choices=(("register","注册激活"),("forget","忘记密码"),("change","修改密码")),max_length=15,verbose_name="发送认证码")
    add_time = models.DateTimeField(verbose_name="发送时间",default=datetime.now)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "邮箱认证码"
        verbose_name_plural = verbose_name

class Feedback(models.Model):
    contact = models.CharField(blank=True, null=True, max_length=20)
    content = models.CharField(blank=True, null=True, max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = "v_feedback"
        verbose_name = "反馈信息"
        verbose_name_plural = verbose_name