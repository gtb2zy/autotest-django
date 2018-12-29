from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

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
    return render(request, 'home.html')


# 退出
def logout(request):
    auth.logout(request)

    # response = HttpResponseRedirect('/login/')
    # return response
    return render(request, 'login.html')
