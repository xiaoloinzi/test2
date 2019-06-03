from sign.models import Event,Guest
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.shortcuts import get_object_or_404


# Create your views here.
# 手动添加了test/123456test
def index(request):
    return render(request,'index.html')

def login_action(request):
    if request.method == "POST":
        username = request.POST.get("username",'')
        password = request.POST.get("password",'')
        # 获取输入的登录名和密码进行验证
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            # 登陆
            auth.login(request,user)
        # if username == "admin" and password == "admin123":
            # HttpResponseRedirect--对路径进行重定向，将请求指向某个目录
            # return HttpResponseRedirect('/event_manage/')
            # response = HttpResponseRedirect('/event_manage/')
            # 添加浏览器cookie
            # response.set_cookie('user',username,3600)
            # 将session信息记录到浏览器
            request.session['user'] = username
            response = HttpResponseRedirect('/event_manage/')

            return response
        else:
            return render(request,'index.html',{'error':'username or password error!'})

# 创建event_manage函数，用于返回发布会管理页面event_manage.html
@login_required#如果要限制某个视图函数必须登陆才能访问，则只需在这个函数前面添加@login_required的装饰即可
def event_manage(request):
    # 读取浏览器cookie
    # username = request.COOKIES.get('user','')
    event_list = Event.objects.all()
    username = request.session.get('user','')

    return render(request,'event_manage.html',{'user':username,"events":event_list})

# 发布会名单搜索
@login_required
def search_name(request):
    username = request.session.get('user','')
    search_name = request.GET.get('name','')
    event_list = Event.objects.filter(name__contains = search_name)
    return render(request,"event_manage.html",{"user":username,"events":event_list})

# 嘉宾管理
@login_required
def guest_manage(request):
    username = request.session.get('user','')
    # 导入Model中的Guest类，通过Guest,objects.all()查询所有对象嘉宾对象（数据），
    # 并通过render()方法附加在guest_manage.html页面，并返回客户端
    guest_list = Guest.objects.all()
    paginator = Paginator(guest_list,2)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
    #     如果page不是整数，取第一面数据
        contacts = paginator.page(paginator.num_pages)

    return render(request,"guest_manage.html",{"user":username,"guests":contacts})

# 签到界面
@login_required
def sign_index(request,eid):
    event = get_object_or_404(Event,id=eid)
    return render(request,'sign_index.html',{"event":event})

# 签到的动作
@login_required
def sign_index_action(request,event_id):
    event = get_object_or_404(Event,id = event_id)
    sign_list = Guest.objects.filter(sign='1',event_id=event_id)
    guest_list = Guest.objects.filter(event_id=event_id)
    guest_date = str(len(guest_list))
    sign_date = str(len(sign_list)+1)
    phone = request.POST.get('phone','')
    print(phone)
    # 判断手机是否存在
    result = Guest.objects.filter(phone=phone)
    if not result:
        return render(request,'sign_index_.html',{'event':event,'hint':'phone error.'})
    # 通过手机和id查询Guest表，查看结果是否为空
    result = Guest.objects.filter(phone=phone,event_id=event_id)
    if not result:
        return render(request,'sign_index.html',{'event':event,'hint':'event id or phone error.'})

    result = Guest.objects.get(phone=phone,event_id=event_id)

    if result.sign:
        # sign = Guest.objects.filter(event_id=eid,sign='1').count()
        return render(request,'sign_index.html',{'event':event,
                                                 'hint':"user has sign in.",
                                                 'guest':guest_date,
                                                 'sign':sign_date,})
    else:
        # sign = Guest.objects.filter(event_id=eid,sign='1').count()
        # 判断嘉宾的签到状态是否为True
        Guest.objects.filter(phone=phone,event_id=event_id).update(sign='1')
        return render(request,'sign_index.html',{'event':event,
                                                 'hint':'sign in success!',
                                                 'guest':guest_date,
                                                 'sign':sign_date,
                                                'user':result})

# 发布会界面和嘉宾界面的退出系统按钮
@login_required
def logout(request):
    auth.logout(request)
    response = HttpResponseRedirect('/index/')
    return response




