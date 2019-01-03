from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from apitest.tests import test_apis
from django.utils import timezone
from .models import LoginRecord
import datetime

# Create your views here.


# 用户登陆
def login(request):
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            request.session['user'] = username
            # home.html 首页
            response = HttpResponseRedirect('/user/home/')
            return response
        else:
            return render(request, 'login.html', {'error': '用户名或密码错误'})
    return render(request, 'login.html')


# 首页
@login_required
def home(request):
    # 测试API
    test_apis()
    # 统计访问人数
    date = timezone.now().date()
    login_num = []
    login_times = []
    for i in range(6, -1, -1):
        login_time = date - datetime.timedelta(days=i)
        try:
            login_record = LoginRecord.objects.get(login_time=login_time)
        except Exception:
            login_record = LoginRecord(login_num=0, login_time=login_time)
        login_num.append(login_record.login_num)
        login_times.append(login_time.strftime('%m/%Y'))
    
    context = {}
    context['login_num'] = login_num
    context['login_times'] = login_times
    return render(request, 'home.html', context)


# 退出
def logout(request):
    auth.logout(request)

    # response = HttpResponseRedirect('/login/')
    # return response
    return render(request, 'login.html')
