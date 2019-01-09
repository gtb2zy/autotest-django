from django.shortcuts import render
from product.models import Product
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import ProductForm
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User


# Create your views here.
@login_required
def product_manage(request):
    username = request.session.get('user', '')
    search_productname = request.GET.get('productname', '')
    product_list = Product.objects.filter(
        productname__icontains=search_productname)
    # 生成paginator对象,设置每页显示5条记录
    paginator = Paginator(product_list, 5)
    # 获取当前的页码数,默认为第1页
    page = request.GET.get('page', 1)
    # 把获取的当前页码数转换成整数类型
    currentPage = int(page)
    try:
        # 获取当前页码数的记录列表
        product_list = paginator.page(currentPage)
    except PageNotAnInteger:
        # 如果输入的页数不是整数则显示第1页的内容
        product_list = paginator.page(1)
    except EmptyPage:
        # 如果输入的页数不在系统的页数中则显示最后一页的内容
        product_list = paginator.page(paginator.num_pages)

    # 获取当前页面前后两页的页码
    page_nums = paginator.num_pages  # 总页数
    page_num = product_list.number  # 当前页
    page_range = [
        x for x in range(int(page_num) - 2,
                         int(page_num) + 3) if 0 < x <= page_nums
    ]
    # 给页码加首页和尾页，间隔页加'...'
    if page_range[0] - 1 > 1:
        page_range.insert(0, '...')
    if page_range[-1] + 1 < page_nums:
        page_range.append('...')
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != page_nums:
        page_range.append(page_nums)
    
    product_form = ProductForm()
    context = {}
    context['user'] = username
    context['products'] = product_list
    context['page_range'] = page_range
    context['product_form'] = product_form
    return render(request, "product_manage.html", context)


# 新增产品
@login_required
def add(request):
    if request.POST:
        product_form = ProductForm(request.POST)
        # 必须先判断is_valid()，否则cleaned_data不存在
        if product_form.is_valid():
            product_form.cleaned_data['creater'] = request.user
            product_form.save()
            return HttpResponseRedirect('/product/list')

        else:
            # 产品名已存在
            print('产品名已存在')
            return HttpResponseRedirect('/product/list')


# 搜索功能
@login_required
def search(request):
    productname = request.GET.get('productname', '')
    return HttpResponseRedirect('/product/list?productname=%s' % (productname))


# 删除产品
def delete(request):
    if request.user == User.objects.all()[0]:
        pk = request.GET.get('pk', '')
        product = Product.objects.filter(pk=pk)
        product.delete()
    return HttpResponseRedirect('/product/list')
