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
from videos.views import IndexView
import xadmin
urlpatterns = [
    #path('admin/', admin.site.urls),
    url(r"^xadmin/",xadmin.site.urls),
    url(r'^captcha/',include('captcha.urls')),
    url(r'^$',IndexView.as_view(), name='index'),
    url(r'^users/',include(('users.urls','users'),namespace="users")),
    url(r"^videos/",include(('videos.urls','videos'),namespace='videos')),
    url(r"^comments/", include(('comments.urls', 'comments'), namespace='comments')),
    url(r"^forums/",include(('forums.urls','forums'),namespace='forums')),
]
