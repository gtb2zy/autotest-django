from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from apitest.tests import test_apis
from django.utils import timezone
from .models import LoginRecord
from django.contrib.auth.models import User
import datetime

# from django.core.cache import cache

# Create your views here.


# 用户登陆
def login(request):
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        # 验证用户密码是否正确
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            # 用户密码正确，登陆
            auth.login(request, user)
            request.session['user'] = username
            # 添加一次流量记录，并加入cookie记录，防止刷记录
            if not request.COOKIES.get(username):
                date = timezone.now().date()
                login_record, _ = LoginRecord.objects.get_or_create(
                    login_time=date)
                login_record.login_num += 1
                login_record.save()
            # home.html 首页
            response = HttpResponseRedirect('/user/home/')
            response.set_cookie(username, 'true', max_age=600)
            return response
        else:
            return render(request, 'login.html', {'error': '用户名或密码错误'})

    else:
        return render(request, 'login.html')


# 首页
@login_required
def home(request):
    # 测试API
    if not request.COOKIES.get('test_apis'):
        test_apis()
    # 统计最近七天的访问人数
    date = timezone.now().date()
    login_num = []
    login_times = []
    for i in range(6, -1, -1):
        login_time = date - datetime.timedelta(days=i)
        login_record, _ = LoginRecord.objects.get_or_create(
            login_time=login_time)
        login_num.append(login_record.login_num)
        login_times.append(login_time.strftime('%Y/%m/%d'))

    context = {}
    context['login_num'] = login_num
    context['login_times'] = login_times
    response = render(request, 'home.html', context)
    response.set_cookie('test_apis', 'true', max_age=600)
    return response


# 退出
def logout(request):
    auth.logout(request)

    # response = HttpResponseRedirect('/login/')
    # return response
    return render(request, 'login.html')


# 注册
def register(request):
    if request.POST:
        try:
            # 验证用户名
            username = request.POST.get('username', '')
            if User.objects.filter(username=username).exists():
                raise Exception('用户名已存在')
            # 验证邮箱
            email = request.POST.get('email', '')
            if User.objects.filter(email=email).exists():
                raise Exception('邮箱已存在')
            # 验证输入密码
            password = request.POST.get('password', '')
            password_again = request.POST.get('password_again', '')
            if password != password_again:
                raise Exception('两次输入密码不一致')

            # 注册新用户
            user = User()
            user.username = username
            user.email = email
            user.set_password(password)
            user.save()
        except Exception as e:
            return render(request, 'register.html', {'error': e})

        # 注册成功，跳转到首页
        return HttpResponseRedirect('/user/home/')
    else:
        return render(request, 'register.html')
