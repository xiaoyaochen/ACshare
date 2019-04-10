"""ACshare URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
from django.conf.urls import url,include

from users.views import *

urlpatterns = [
    # url(r'^xadmin/', xadmin.site.urls),
    url(r'^user_register/$',user_register,name='user_register'),
    url(r'^user_login/$',user_login,name="user_login"),
    url(r'^user_logout/$',user_logout,name="user_logout"),
    url(r'^user_active/(\w+)/$',user_active,name="user_active"),
    url(r'^user_forget/$',user_forget,name="user_forget"),
    url(r'^user_reset/(\w+)/$',user_reset,name="user_reset"),
    path('profile/<int:pk>/',ProfileView.as_view(),name="profile"),
    path('change_password/',change_password,name="change_password"),
    path('subscribe/<int:pk>/',SubscribeView.as_view(),name="subscribe"),
    path('feedback/',FeedbackView.as_view(),name="feedback"),
    path('<int:pk>/collect_videos/',CollectListView.as_view(),name='collect_videos'),
    path('<int:pk>/like_videos/',LikeListView.as_view(),name='like_videos'),
    path('up_men',up_men,name="up_men"),
    path('search',up_men,name="search"),
    url(r'^up_men_detail/(\d+)/$',up_men_detail,name="up_men_detail"),
]
