# Generated by Django 2.0 on 2019-03-17 00:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Classification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True, verbose_name='类型名')),
                ('status', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': '视频类型',
                'verbose_name_plural': '视频类型',
            },
        ),
        migrations.CreateModel(
            name='VideoInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True, verbose_name='视频标题')),
                ('desc', models.CharField(blank=True, max_length=255, null=True, verbose_name='视频描述')),
                ('file', models.FileField(max_length=255, upload_to='', verbose_name='视频文件')),
                ('cover', models.ImageField(blank=True, null=True, upload_to='cover/', verbose_name='视频封面')),
                ('status', models.CharField(choices=[('1', '发布中'), ('0', '未发布')], default='0', max_length=1, verbose_name='视频状态')),
                ('add_time', models.DateTimeField(auto_now_add=True, max_length=20, verbose_name='添加时间')),
                ('blong', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='up主')),
                ('classification', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='videos.Classification', verbose_name='视频类型')),
            ],
            options={
                'verbose_name': '视频信息',
                'verbose_name_plural': '视频信息',
            },
        ),
    ]
