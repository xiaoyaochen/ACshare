# Generated by Django 2.0 on 2019-03-18 23:16

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='comment',
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='avatar',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='nickname',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
