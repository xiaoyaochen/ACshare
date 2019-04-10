# Generated by Django 2.0 on 2019-03-25 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_feedback'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='feedback',
            options={'verbose_name': '反馈信息', 'verbose_name_plural': '反馈信息'},
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.FileField(upload_to='users/%y/%m/%d', verbose_name='用户头像'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', '男'), ('F', '女')], max_length=1, null=True, verbose_name='用户性别'),
        ),
    ]
