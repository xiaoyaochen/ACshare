from django.shortcuts import render,reverse,redirect
from django.http import JsonResponse
from .models import *
from django.core.paginator import PageNotAnInteger,EmptyPage,Paginator
from django.views.decorators.http import require_http_methods
from helpers import ajax_required
from django.views import generic
from forums.forms import ForumsForm
from django.contrib import messages
from ratelimit.decorators import ratelimit
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
def ForumsView(request):
    forums_list = Forums.objects.all()
    keyword = request.GET.get('keywords','')
    if keyword:
        forums_list = forums_list.filter(title__contains=keyword)
    sort = request.GET.get('sort','')
    if sort:
        forums_list = forums_list.order_by('-'+sort)
    pagenum = request.GET.get('pagenum','')
    pa = Paginator(forums_list,8)
    try:
        pages = pa.page(pagenum)
    except PageNotAnInteger:
        pages = pa.page(1)
    except EmptyPage:
        pages = pa.page(pa.num_pages)
    return render(request,'forums/forums_list.html',{'forums_list':forums_list,
                                                     'pages':pages,
                                                     'keywords':keyword,
                                                     'sort':sort})


def Forums_detailView(request,forums_id):
    forums_list = Forums.objects.filter(pk=forums_id)
    forums_obj = forums_list[0]
    forums_obj.view_count += 1
    forums_obj.save(update_fields=['view_count'])
    # comment_list = ForumsComment.objects.filter(forums=forums_id)
    return render(request,"forums/forums_detail.html",{"forums_obj":forums_obj,
                                                       # "comment_list":comment_list
                                                       })



@ajax_required
@require_http_methods(["POST"])
def like(request):
    if not request.user.is_authenticated:
        return JsonResponse({"code": 1, "msg": "请先登录"})
    forums_id = request.POST['forums_id']
    forums = Forums.objects.get(pk=forums_id)
    forums.up_count += 1
    forums.save(update_fields=['up_count'])
    return JsonResponse({"code":0, "likes":forums.up_count, "user_liked": 0})


class Forums_createView(LoginRequiredMixin,generic.CreateView):
    login_url = "users:user_login"
    model = Forums
    form_class = ForumsForm
    template_name = "forums/forums_create.html"

    # def get_form_kwargs(self):
    #     kwargs = super(Forums_createView, self).get_form_kwargs()
    #     kwargs.update({
    #         'user':self.request.user,
    #     })
    #     return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        messages.success(self.request, "提交成功")
        return redirect('forums:forums_create')

    @ratelimit(key='ip',rate='2/m')
    def post(self, request, *args, **kwargs):
        was_limited = getattr(request, 'limited', False)
        if was_limited:
            messages.warning(self.request, "操作太频繁了，请1分钟后再试")
            return render(request, 'forums/forums_create.html', {'form': ForumsForm()})
        return super().post(request,*args,**kwargs)

    def get_success_url(self):
        messages.success(self.request, "提交成功")
        return reverse('forums:forums_list')