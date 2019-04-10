from django.shortcuts import render
from videos.forms import CommentForm
from videos.models import VideoInfo
from datetime import datetime
from django.shortcuts import *
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.http import HttpResponseBadRequest,JsonResponse
from django.template.loader import render_to_string
from ratelimit.decorators import ratelimit
# Create your views here.

@ratelimit(key='ip',rate='2/m')
def submit_comment(request,pk):
    '''
    每分钟限制发2条
    '''
    was_limited = getattr(request,'limited',False)
    if was_limited:
        return JsonResponse({"code":1,'msg':'评论太频繁了，请1分钟后再试'})
        pass
    video = get_object_or_404(VideoInfo,pk=pk)
    form = CommentForm(data=request.POST)

    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.user = request.user
        new_comment.nickname = request.user.nick_name
        new_comment.avatar = request.user.avatar
        new_comment.video = video
        new_comment.save()

        data = dict()
        # data['nick_name'] = request.user.nick_name
        # data['avatar'] = request.user.avatar
        data['user'] = request.user
        data['add_time'] = datetime.fromtimestamp(datetime.now().timestamp())
        data['content'] = new_comment.content
        comments = list()
        comments.append(data)
        html = render_to_string(
            "comment/comment_single.html",{"comments":comments}
        )
        return JsonResponse({"code":0,"html":html})
    return JsonResponse({"code":1,'msg':"评论失败！"})


def get_comments(request):
    if not request.is_ajax():
        return HttpResponseBadRequest()
    page = request.GET.get('page')
    page_size = request.GET.get('page_size')
    video_id  = request.GET.get("video_id")
    video = get_object_or_404(VideoInfo,pk=video_id)
    comments = video.comment_set.order_by('-add_time').all()
    comment_count = len(comments)
    print(comments[0])
    paginator = Paginator(comments,page_size)
    try:
        rows = paginator.page(page)
    except PageNotAnInteger:
        rows = paginator.page(1)
    except EmptyPage:
        rows = []

    if len(rows) > 0:
        code = 0
        html = render_to_string(
            "comment/comment_single.html",{"comments":rows}
        )
    else:
        code = 1
        html = ""

    return JsonResponse({
        "code":code,
        "html":html,
        "comment_count":comment_count
    })
