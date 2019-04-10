# Generated by Django 2.0 on 2019-04-08 19:51

import datetime
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
            name='Forums',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20, verbose_name='标题')),
                ('content', models.TextField(verbose_name='内容')),
                ('comment_count', models.IntegerField(default=0)),
                ('up_count', models.IntegerField(default=0)),
                ('pub', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('priority', models.IntegerField(default=1000, verbose_name='优先级')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='作者')),
            ],
            options={
                'verbose_name': '贴子',
                'verbose_name_plural': '贴子',
            },
        ),
        migrations.CreateModel(
            name='ForumsComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=200, verbose_name='评论内容')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('forums', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forums.Forums')),
                ('parent_conment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='forums.ForumsComment')),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='评论者')),
            ],
            options={
                'verbose_name': '评论',
                'verbose_name_plural': '评论',
            },
        ),
        migrations.CreateModel(
            name='ForumsUpDown',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('is_up', models.BooleanField(default=True)),
                ('forums', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='forums.Forums')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='forumsupdown',
            unique_together={('forums', 'user')},
        ),
    ]