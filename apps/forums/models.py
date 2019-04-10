from django.db import models
from users.models import UserProfile
from datetime import datetime
# Create your models here.

class Forums(models.Model):
    title = models.CharField(max_length=20,verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    view_count = models.IntegerField(default=0)
    up_count = models.IntegerField(default=0)
    author = models.ForeignKey(UserProfile,on_delete=models.CASCADE,verbose_name='作者')
    pub = models.DateTimeField(default=datetime.now,verbose_name='添加时间')
    priority = models.IntegerField(default=1000,verbose_name='优先级')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '贴子'
        verbose_name_plural = verbose_name
#
# class ForumsComment(models.Model):
#     content = models.CharField(verbose_name='评论内容',max_length=200)
#     forums = models.ForeignKey(Forums,on_delete=models.CASCADE)
#     user = models.ForeignKey(UserProfile,verbose_name='评论者',on_delete=models.CASCADE)
#     add_time = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)
#     parent_conment = models.ForeignKey('self',null=True,on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.content
#
#     class Meta:
#         verbose_name = '评论'
#         verbose_name_plural = verbose_name
#
# class ForumsUpDown(models.Model):
#     nid = models.AutoField(primary_key=True)
#     user = models.ForeignKey(UserProfile,null=True,on_delete=models.CASCADE)
#     forums = models.ForeignKey(Forums,null=True,on_delete=models.CASCADE)
#     is_up = models.BooleanField(default=True)
#
#     class Meta:
#         unique_together = [('forums','user'),]
