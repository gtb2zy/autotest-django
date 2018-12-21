from django.shortcuts import render
from apitest.models import Apistep, Apitest, Apis, Apiinfo
import pymysql
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required


# Create your views here.
def test(request):
    # return HttpResponse('Hello test')
    return render(request, 'left.html')


# 接口管理
@login_required
def apitest_manage(request):
    apitest_list = Apitest.objects.all()
    username = request.session.get('user', '')
    apitest_count = apitest_list.count()  # 统计总数
    paginator = Paginator(apitest_list, 8)  # 设置每页显示8条记录
    page = request.GET.get('page', 1)  # 获取当前的页码数,默认为第1页
    currentPage = int(page)  # 把获取的当前页码数转换成整数类型
    try:
        apitest_list = paginator.page(page)  # 获取当前页码数的记录列表
    except PageNotAnInteger:
        apitest_list = paginator.page(1)  # 如果输入的页数不是整数则显示第1页的内容
    except EmptyPage:
        apitest_list = paginator.page(
            paginator.num_pages)  # 如果输入的页数不在系统的页数中则显示最后一页的内容
    return render(
        request, 'apitest_manage.html', {
            'user': username,
            'apitest_count': apitest_count,
            'currentPage': currentPage,
            'apitests': apitest_list,
        })


# 接口步骤管理
@login_required
def apistep_manage(request):
    username = request.session.get('user', '')
    apitestid = request.GET.get('apitest.id', None)
    apitest = Apitest.objects.get(id=apitestid)
    apistep_list = Apistep.objects.all()  # 获取所有接口测试用例
    return render(request, "apistep_manage.html", {
        "user": username,
        "apitest": apitest,
        "apisteps": apistep_list
    })


# API测试用例
@login_required
def apis_manage(request):
    apis_list = Apis.objects.all()
    username = request.session.get('user', '')
    apis_count = apis_list.count()  # 统计产品数
    paginator = Paginator(apis_list, 8)  # 生成paginator对象,设置每页显示8条记录
    page = request.GET.get('page', 1)  # 获取当前的页码数,默认为第1页
    currentPage = int(page)  # 把获取的当前页码数转换成整数类型
    try:
        apis_list = paginator.page(page)  # 获取当前页码数的记录列表
    except PageNotAnInteger:
        apis_list = paginator.page(1)  # 如果输入的页数不是整数则显示第1页的内容
    except EmptyPage:
        apis_list = paginator.page(
            paginator.num_pages)  # 如果输入的页数不在系统的页数中则显示最后一页的内容
    return render(
        request, "apis_manage.html", {
            "user": username,
            "apiss": apis_list,
            "currentPage": currentPage,
            "apiscounts": apis_count
        })  # 把值赋给apiscounts这个变量


# API具体内容
@login_required
def apiinfos_manage(request):
    user = request.session.get('user', '')
    apisid = request.GET.get('apis.id', None)
    apis = Apis.objects.get(id=apisid)
    apiinfos_list = Apiinfo.objects.all()
    return render(request, 'apiinfos_manage.html', {
        'user': user,
        'apis': apis,
        'apiinfos': apiinfos_list,
    })


# 搜索功能-流程接口测试
@login_required
def apisearch(request):
    username = request.session.get('user', '')
    search_apitestname = request.GET.get('apitestname', '')
    apitest_list = Apitest.objects.filter(
        apitestname__icontains=search_apitestname)
    return render(request, 'apitest_manage.html', {
        'user': username,
        'apitests': apitest_list,
    })


# 搜索功能-流程接口测试步骤
@login_required
def apistepsearch(request):
    username = request.session.get('user', '')
    search_apiname = request.GET.get('apiname', '')
    apistep_list = Apistep.objects.filter(apiname__icontains=search_apiname)
    return render(request, 'apistep_manage.html', {
        'user': username,
        'apisteps': apistep_list,
    })


# 搜索功能-单一接口测试
@login_required
def apissearch(request):
    username = request.session.get('user', '')
    search_apiname = request.GET.get('apiname', '')
    apis_list = Apis.objects.filter(apiname__icontains=search_apiname)
    return render(request, 'apis_manage.html', {
        'user': username,
        'apiss': apis_list,
    })


# 测试报告
@login_required
def test_report(request):
    username = request.session.get('user', '')
    apis_list = Apis.objects.all()
    apis_count = apis_list.count()
    db = pymysql.connect(
        user='root', db='autotest', passwd='test123456', host='127.0.0.1')
    cursor = db.cursor()
    sql1 = 'SELECT count(id) FROM apitest_apis WHERE apitest_apis.apistatus=1'
    aa = cursor.execute(sql1)
    apis_pass_count = [row[0] for row in cursor.fetchmany(aa)][0]
    sql2 = 'SELECT count(id) FROM apitest_apis WHERE apitest_apis.apistatus=0'
    bb = cursor.execute(sql2)
    apis_fail_count = [row[0] for row in cursor.fetchmany(bb)][0]
    db.close()
    return render(
        request, "report.html", {
            'user': username,
            "apiss": apis_list,
            "apiscounts": apis_count,
            "apis_pass_counts": apis_pass_count,
            "apis_fail_counts": apis_fail_count
        })  # 把值赋给apiscounts这个变量
