# Generated by Django 2.0 on 2019-04-01 15:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0002_auto_20190318_2316'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='nickname',
        ),
    ]
