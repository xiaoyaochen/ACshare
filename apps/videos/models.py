from django.db import models
from users.models import UserProfile
from ACshare import settings
from chunked_upload.models import ChunkedUpload
import os
from django.dispatch import receiver
# Create your models here.

class VideoInfoQuerySet(models.query.QuerySet):
    def get_count(self):
        return self.count()

    def get_pubulished_count(self):
        return self.filter(status=1).count()

    def get_not_published_count(self):
        return self.filter(status=0).count()

    def get_published_list(self):
        return self.filter(status=1).order_by('-add_time')

    def get_search_list(self,keyword):
        if keyword:
            return self.filter(title__contans=keyword).order_by('-add_time')
        else:
            return self.order_by('-add_time')

    def get_recommend_list(self):
        return self.filter(status=1).order_by('-view_count')[:4]




class Classification(models.Model):
    list_display = ("title",)
    title = models.CharField(max_length=100,null=True,blank=True,verbose_name="类型名")
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "视频类型"
        verbose_name_plural = verbose_name


class VideoInfo(models.Model):
    title = models.CharField(max_length=100,null=True,blank=True,verbose_name="视频标题")
    desc = models.CharField(max_length=255,null=True,blank=True,verbose_name="视频描述")
    classification = models.ForeignKey(Classification,on_delete=models.CASCADE,null=True,verbose_name='视频类型')
    file = models.FileField(upload_to="video/%y/%m/%d",max_length=255,verbose_name="视频文件")
    cover = models.ImageField(upload_to="cover/%y/%m/%d",null=True,blank=True,verbose_name="视频封面")
    status = models.CharField(choices=(('1','发布中'),('0','未发布')),max_length=1,default='0',verbose_name='视频状态')
    view_count = models.IntegerField(default=0,blank=True,verbose_name='点击量')
    collected = models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,related_name="collected_video")
    liked = models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,related_name="liked_video")

    up_man = models.ForeignKey(UserProfile,on_delete=models.CASCADE,null=True,verbose_name="up主")
    add_time = models.DateTimeField(auto_now_add=True,blank=True,verbose_name="添加时间",max_length=20)
    objects = VideoInfoQuerySet.as_manager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "视频信息"
        verbose_name_plural = verbose_name

    def increase_view_count(self):
        self.view_count += 1
        self.save(update_fields=['view_count'])

    def switch_like(self,user):
        if user in self.liked.all():
            self.liked.remove(user)
        else:
            self.liked.add(user)
    def count_likers(self):
        return self.liked.count()

    def user_liked(self,user):
        if user in self.liked.all():
            return 0
        else:
            return 1
    def switch_collect(self,user):
        if user in self.collected.all():
            self.collected.remove(user)
        else:
            self.collected.add(user)
            print(2)

    def count_collecters(self):
        return self.collected.count()

    def user_collected(self,user):
        if user in self.collected.all():
            return 0
        else:
            return 1
    def user_up_count(self):
        obj =  UserProfile.objects.filter(id=self.up_man.id)
        print(obj)
        obj.up_count += 1
        obj.save(update_fields=["up_count"])


@receiver(models.signals.post_delete, sender=VideoInfo)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    删除FileField文件
    """
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)




class MyChunkedUpload(ChunkedUpload):
    pass

MyChunkedUpload._meta.get_field('user').null = True