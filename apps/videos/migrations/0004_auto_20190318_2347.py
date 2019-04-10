# Generated by Django 2.0 on 2019-03-18 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0003_auto_20190318_1304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videoinfo',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to='cover/%y/%m/%d', verbose_name='视频封面'),
        ),
        migrations.AlterField(
            model_name='videoinfo',
            name='file',
            field=models.FileField(max_length=255, upload_to='video/%y/%m/%d', verbose_name='视频文件'),
        ),
    ]