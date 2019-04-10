from django.shortcuts import render
from django.views import generic
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from chunked_upload.views import ChunkedUploadView,ChunkedUploadCompleteView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from helpers import get_page_list,ajax_required,AuthorRequiredMixin
from .forms import *
from users.models import BannerInfo
from django.views.generic import TemplateView
from django.urls import reverse
from django.contrib import messages
# Create your views here.
# def index(request):
#     return render(request,'videos/index.html')

class IndexView(generic.ListView):
    model = VideoInfo
    template_name = 'videos/index.html'
    context_object_name = 'video_list'
    paginate_by = 12
    c = None

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(IndexView,self).get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        page_list = get_page_list(paginator,page)
        # classification_list = Classification.objects.filter(status=True).values()
        # context['c'] = self.c
        # context['classification_list'] = classification_list
        all_banners = BannerInfo.objects.all().order_by('-add_time')
        context['page_list'] = page_list
        context['all_banners'] = all_banners
        return context

    def get_queryset(self):
        # self.c = self.request.GET.get('c',None)
        # if self.c:
        #     classification = get_object_or_404(Classification,pk=self.c)
        #     return classification.videoinfo_set.all().order_by('-add_time')
        # else:
        return VideoInfo.objects.filter(status=1).order_by('-add_time')

class AdVideo(generic.ListView):
    model = VideoInfo
    template_name = 'videos/ad_video.html'
    context_object_name = 'video_list'
    paginate_by = 12
    c = None
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AdVideo, self).get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        page_list = get_page_list(paginator,page)
        classification_list = Classification.objects.filter(status=True).values()
        context['c'] = self.c
        context['classification_list'] = classification_list
        context['page_list'] = page_list
        return context

    def get_queryset(self):
        self.c = self.request.GET.get('c', None)
        if self.c:
            classification = get_object_or_404(Classification, pk=self.c)
            return classification.videoinfo_set.filter(status=1).order_by('-add_time')
        else:
            return VideoInfo.objects.filter(status=1).order_by('-add_time')


class SearchListView(generic.ListView):
    model = VideoInfo
    template_name = 'videos/search.html'
    context_object_name = "video_list"
    paginate_by = 8
    keywords = ''

    def get_queryset(self):
        self.keywords = self.request.GET.get("keywords",'')
        return VideoInfo.objects.filter(title__contains=self.keywords).filter(status=1)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SearchListView,self).get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        page_list = get_page_list(paginator,page)
        context['page_list'] = page_list
        context['keywords'] = self.keywords
        return context

class VideoDetailView(generic.DetailView):
    model = VideoInfo
    template_name = "videos/detail.html"

    def get_object(self, queryset=None):
        obj = super(VideoDetailView,self).get_object()
        obj.increase_view_count()
        return obj

    def get_context_data(self, **kwargs):
        context = super(VideoDetailView,self).get_context_data(**kwargs)
        form = CommentForm()
        recommend_list = VideoInfo.objects.get_recommend_list()
        context['form'] = form
        context['recommend_list'] = recommend_list
        return context




@ajax_required
@require_http_methods(["POST"])
def like(request):
    if not request.user.is_authenticated:
        return JsonResponse({"code": 1, "msg": "请先登录"})
    video_id = request.POST['video_id']
    video = VideoInfo.objects.get(pk=video_id)
    user = request.user
    video.switch_like(user)
    return JsonResponse({"code":0, "likes": video.count_likers(), "user_liked": video.user_liked(user)})


@ajax_required
@require_http_methods(["POST"])
def collect(request):
    if not request.user.is_authenticated:
        return JsonResponse({"code": 1, "msg": "请先登录"})
    video_id = request.POST['video_id']
    video = VideoInfo.objects.get(pk=video_id)
    user = request.user
    video.switch_collect(user)
    return JsonResponse({"code":0, "collects": video.count_collecters(), "user_collected": video.user_collected(user)})


class AddVideoView(LoginRequiredMixin,TemplateView):
    template_name = 'videos/video_add.html'




class MyChunkedUploadView(ChunkedUploadView):
    model = MyChunkedUpload
    field_name = 'the_file'


class MyChunkedUploadCompleteView(ChunkedUploadCompleteView):
    model = MyChunkedUpload

    def on_completion(self, uploaded_file, request):
        print("upload------->",uploaded_file.name)
        pass
    def get_response_data(self, chunked_upload, request):
        video = VideoInfo.objects.create(file=chunked_upload.file)
        return {'code':0,'video_id':video.id,'msg':'success'}

class VideoPublishView(LoginRequiredMixin,generic.UpdateView):
    model = VideoInfo
    form_class = VideoPublishForm
    template_name = 'videos/video_publish.html'

    def get_context_data(self, **kwargs):
        context = super(VideoPublishView,self).get_context_data(**kwargs)
        clf_list = Classification.objects.all().values()
        clf_data = {"clf_list":clf_list}
        context.update(clf_data)
        return context

    def get_form_kwargs(self):
        kwargs = super(VideoPublishView, self).get_form_kwargs()
        kwargs.update({
            'user':self.request.user
        })
        return kwargs

    # def get_form(self, form_class=None):
    #     return self.form_class(self.request.user, **self.get_form_kwargs())

    def get_success_url(self):
        all_obj = UserProfile.objects.filter(username=self.request.user)
        obj = all_obj[0]
        obj.up_count += 1
        obj.save(update_fields=['up_count'])
        print(obj.up_count)
        return reverse('videos:video_publish_success')


class VideoPublishSuccessView(LoginRequiredMixin,TemplateView):
    template_name = 'videos/video_publish_success.html'


class VideoListView(LoginRequiredMixin,generic.ListView):
    model = VideoInfo
    template_name = 'videos/video_list.html'
    context_object_name = 'video_list'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(VideoListView, self).get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        page_list = get_page_list(paginator,page)
        context['page_list'] = page_list
        return context
    def get_queryset(self):
        return VideoInfo.objects.filter(up_man=self.request.user)


class VideoEditView(LoginRequiredMixin,AuthorRequiredMixin,generic.UpdateView):
    model = VideoInfo
    form_class = VideoEditForm
    template_name = 'videos/video_edit.html'

    def get_context_data(self, **kwargs):
        context = super(VideoEditView, self).get_context_data(**kwargs)
        clf_list = Classification.objects.all().values()
        clf_data = {'clf_list':clf_list}
        context.update(clf_data)
        return context
    def get_success_url(self):
        messages.success(self.request,'保存成功')
        return reverse('videos:video_edit',kwargs={'pk':self.kwargs['pk']})



@ajax_required
@require_http_methods(['POST'])
def video_delete(request):
    video_id = request.POST['video_id']
    instance = VideoInfo.objects.get(id=video_id)
    instance.delete()
    return JsonResponse({'code':0,'msg':'success'})