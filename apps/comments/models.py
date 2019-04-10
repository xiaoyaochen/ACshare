from django.db import models

# Create your models here.
import datetime

from django.conf import settings
from videos.models import VideoInfo
class CommentQuerySet(models.query.QuerySet):
    def get_count(self):
        return self.count()
    def get_today_count(self):
        return self.exclude(timestamp__lt=datetime.date.today()).count()

class Comment(models.Model):
    list_display = ("content","add_time",)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    avatar = models.CharField(max_length=100,blank=True,null=True)
    video = models.ForeignKey(VideoInfo,on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    add_time = models.DateTimeField(auto_now_add=True)
    object = CommentQuerySet.as_manager()
    class Meta:
        verbose_name = "视频评论"
        verbose_name_plural = verbose_name