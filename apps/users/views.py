from django.shortcuts import render,redirect,reverse,HttpResponse
from .forms import UserRegisterForm,UserLoginForm,UserForgetForm,UserResetForm,ProfileForm,ChangeePwdForm
from .forms import SubscribeForm,FeedbackForm
from .models import UserProfile,EmailVerification,Feedback,BannerInfo
from django.db.models import Q
from django.contrib.auth import authenticate,login,logout
from tools.sendEmail import send_email
from django.contrib.auth import get_user_model,update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from ratelimit.decorators import ratelimit
from helpers import get_page_list,AuthorRequiredMixin
from django.views import generic
from django.contrib import messages
from django.shortcuts import *
from django.core.paginator import PageNotAnInteger,Paginator,EmptyPage
# Create your views here.

# def index(request):
#     return render(request,"users/index.html")
#
User = get_user_model()
def user_register(request):
    all_banners = BannerInfo.objects.all().order_by('-add_time')
    if request.method == "GET":
        user_register_form = UserRegisterForm()
        return render(request,"users/register.html",{
            "user_register_form":user_register_form,
            "all_banners":all_banners
        })
    else:
        user_register_form = UserRegisterForm(request.POST)
        if user_register_form.is_valid():
            email = user_register_form.cleaned_data["email"]
            password = user_register_form.cleaned_data["password"]

            user_list = UserProfile.objects.filter(Q(username= email)|Q(email=email) )
            if user_list:
                return  render(request,'users/register.html',{
                    'msg':"用户已经存在",
                    "all_banners": all_banners
                })
            else:
                a = UserProfile()
                a.username = email
                a.set_password(password)
                a.email = email
                a.save()

                send_email(email,1)
                return HttpResponse("请去邮箱激活账户，否则无法登陆！<a href=''>返回</a>")
                #return redirect(reverse('index'))
        else:
            return render(request,"users/register.html",{
                'user_register_form':user_register_form,
                "all_banners": all_banners
            })


def user_login(request):
    all_banners = BannerInfo.objects.all().order_by('-add_time')
    if request.method == "GET":
        user_login_form = UserLoginForm()
        return render(request,"users/login.html",{
            "user_login_form":user_login_form,
            "all_banners":all_banners
        })
    else :
        user_login_form = UserLoginForm(request.POST)
        if user_login_form.is_valid():
            username = user_login_form.cleaned_data['username']
            password = user_login_form.cleaned_data['password']

            user = authenticate(username=username,password=password)
            if user:
                if user.is_start:
                    login(request,user)
                    print("登陆成功")
                    return redirect(reverse("index"))
                else:
                    return HttpResponse("请去邮箱激活账户，否则无法登陆！<a href=''>返回</a>")
            else:
                return render(request,'users/login.html',{
                    'msg':"账户或密码错误！"

                })
        else:
            return render(request, 'users/login.html', {
                'user_login_form': user_login_form,
                "all_banners": all_banners
                })

def user_logout(request):
    logout(request)
    return redirect(reverse("users:user_login"))


def user_active(request,code):
    if code:
        email_ver_list = EmailVerification.objects.filter(code=code)
        if email_ver_list:
            email_ver = email_ver_list[0]
            email = email_ver.email
            user_list = UserProfile.objects.filter(username=email)
            if user_list:
                user = user_list[0]
                user.is_start = True
                user.save()
                return redirect(reverse('users:user_login'))
            else:
                pass
        else:
            pass
    else:
        pass

def user_forget(request):
    all_banners = BannerInfo.objects.all().order_by('-add_time')
    if request.method == "GET":
        user_forget_form = UserForgetForm()
        return render(request,'users/forgetpwd.html',{
            'user_forget_form':user_forget_form,
            "all_banners": all_banners
        })
    else:
        user_forget_form = UserForgetForm(request.POST)
        if user_forget_form.is_valid():
            email = user_forget_form.cleaned_data['email']
            user_list = UserProfile.objects.filter(email=email)
            if user_list:
                send_email(email,2)
                return HttpResponse('"请去邮箱修改密码！<a href=''>返回</a>"')
            else:
                return render(request,'users/forgetpwd.html',{
                    'msg':"邮箱不存在"
                })
        else:
            return render(request,'users/forgetpwd.html',{
                'user_forget_form':user_forget_form,
                "all_banners": all_banners
            })
def user_reset(request,code):
    all_banners = BannerInfo.objects.all().order_by('-add_time')
    if request.method == "GET":
        return render(request,'users/password_reset.html',{
            "code":code,
            "all_banners": all_banners
        })
    else:
        user_reset_form = UserResetForm(request.POST)
        if user_reset_form.is_valid():
            password1 = user_reset_form.cleaned_data['password1']
            password2 = user_reset_form.cleaned_data['password2']
            if password1 == password2:
                email_ver_list = EmailVerification.objects.filter(code=code)
                if email_ver_list:
                    username = email_ver_list[0].email
                    user_list = UserProfile.objects.filter(username=username)
                    user = user_list[0]
                    user.set_password(password1)
                    user.save()
                    return redirect(reverse('users:user_login'))
                else:
                    pass
            else:
                return render(request,'users/password_reset.html',{
                "code":code,
                "msg":"前后密码不一致",
                "all_banners": all_banners
                })
        else:
            pass


class ProfileView(LoginRequiredMixin,AuthorRequiredMixin,generic.UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'users/profile.html'

    def get_success_url(self):
        messages.success(self.request,"保存成功")
        return reverse("users:profile",kwargs={'pk': self.request.user.pk})



def change_password(request):
    if request.method == "POST":
        form = ChangeePwdForm(request.user,request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if not user.is_staff and not user.is_superuser:
                user.save()
                update_session_auth_hash(request,user)
                messages.success(request,'修改成功')
                return redirect('users:change_password')
            else:
                messages.warning(request,'无权修改管理员密码')
                return redirect('users:change_password')
        else:
            print(form.errors)
    else:
        form = ChangeePwdForm(request.user)
    return render(request,'users/change_password.html',{
        'form':form
    })


class SubscribeView(LoginRequiredMixin,AuthorRequiredMixin,generic.UpdateView):
    model = User
    form_class = SubscribeForm
    template_name = 'users/subscribe.html'

    def get_success_url(self):
        messages.success(self.request,'保存成功')
        return reverse('users:subscribe',kwargs={'pk':self.request.user.pk})


class FeedbackView(LoginRequiredMixin,generic.CreateView):
    model = Feedback
    form_class = FeedbackForm
    template_name = 'users/feedback.html'

    @ratelimit(key='ip', rate='2/m')
    def post(self, request, *args, **kwargs):
        was_limited = getattr(request, 'limited', False)
        if was_limited:
            messages.warning(self.request, "操作太频繁了，请1分钟后再试")
            return render(request, 'users/feedback.html', {'form': FeedbackForm()})
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, "提交成功")
        return reverse('users:feedback')


class CollectListView(generic.ListView):
    model = User
    template_name = 'users/collect_videos.html'
    context_object_name = 'video_list'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CollectListView,self).get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        page_list = get_page_list(paginator,page)
        context['page_list'] = page_list
        return context
    def get_queryset(self):
        user = get_object_or_404(User,pk=self.kwargs.get('pk'))
        videos = user.collected_video.all()
        return videos

class LikeListView(generic.ListView):
    model = User
    template_name = 'users/like_videos.html'
    context_object_name = 'video_list'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(LikeListView,self).get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        page_list = get_page_list(paginator,page)
        context['page_list'] = page_list
        return context

    def get_queryset(self):
        user = get_object_or_404(User,pk=self.kwargs.get('pk'))
        videos = user.liked_video.all()
        return videos


def up_men(request):
    all_upmen = UserProfile.objects.filter(up_count__gt=0)
    sort_upmen = all_upmen.order_by('-up_count')[:2]
    keyword = request.GET.get('keywords','')
    if keyword:
        all_upmen = all_upmen.filter(nick_name__icontains=keyword)
    sort = request.GET.get('sort','')
    if sort:
        all_upmen = all_upmen.order_by('-'+sort)
    pagenum = request.GET.get('pagenum','')
    pa = Paginator(all_upmen,4)
    try:
        pages = pa.page(pagenum)
    except PageNotAnInteger:
        pages = pa.page(1)
    except EmptyPage:
        pages = pa.page(pa.num_pages)

    return render(request,"users/up_men-list.html",{
        "all_upmen":all_upmen,
        "sort_upmen":sort_upmen,
        "pages":pages,
        'sort':sort,
        "keyword":keyword
    })

def up_men_detail(request,upman_id):
    # return render(request,"users/up_men-detail.html")
    if upman_id:
        all_upmen = UserProfile.objects.filter(up_count__gt=0)
        upman = UserProfile.objects.filter(id=int(upman_id))[0]
        sort_upmem = all_upmen.order_by('-up_count')[:2]
        print(sort_upmem)
    return render(request,"users/up_men-detail.html",{
        'upman':upman,
        'sort_upmen':sort_upmem,
    })
