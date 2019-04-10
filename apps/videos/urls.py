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
from django.urls import path
from django.conf.urls import url,include

from videos.views import *

urlpatterns = [
    url(r"^ad_video/$",AdVideo.as_view(),name="ad_video"),
    url(r"^search/",SearchListView.as_view(),name="search"),
    path("detail/<int:pk>/",VideoDetailView.as_view(),name='detail'),
    path("like/",like,name='like'),
    path('collect/',collect,name='collect'),
    path('video_add/',AddVideoView.as_view(),name="video_add"),
    path('chunked_upload/',MyChunkedUploadView.as_view(),name="api_chunked_upload"),
    path('chunked_upload_complete/',MyChunkedUploadCompleteView.as_view(),name='api_chunked_upload_complete'),
    path('video_publish/<int:pk>',VideoPublishView.as_view(),name = 'video_publish'),
    path('video_publish_success/',VideoPublishSuccessView.as_view(),name='video_publish_success'),
    path('video_list/',VideoListView.as_view(),name='video_list'),
    path('video_delete',video_delete,name='video_delete'),
    path('video_edit/<int:pk>/', VideoEditView.as_view(), name='video_edit'),
]
