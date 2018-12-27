from django.db import models


# Create your models here.
# 流程场景接口
class Apitest(models.Model):
    Product = models.ForeignKey(
        'product.Product', on_delete=models.CASCADE, null=True)  # 关联产品id
    apitestname = models.CharField('流程接口名称', max_length=64)  # 流程接口 测试场景
    apitestdesc = models.CharField('描述', max_length=64, null=True)  # 流程接口 描述
    apitester = models.CharField('测试负责人', max_length=16)  # 执行人
    apitestresult = models.BooleanField('测试结果')  # 流程接口测试结果
    create_time = models.DateTimeField('创建时间', auto_now=True)  # 创建时间-自动获取当前时间

    class Meta:
        verbose_name = '流程场景接口'
        verbose_name_plural = '流程场景接口'

    def __str__(self):
        return self.apitestname


class Apistep(models.Model):
    Apitest = models.ForeignKey(
        'Apitest',
        on_delete=models.CASCADE,
    )  # 关联接口id
    apistep = models.CharField('测试步聚', max_length=100, null=True)  # 测试步聚
    apiname = models.CharField('接口名称', max_length=100)  # 接口名称描述
    apiurl = models.CharField('url地址', max_length=200)  # 地址
    REQUEST_METHOD = (('get', 'get'), ('post', 'post'), ('put', 'put'),
                      ('delete', 'delete'), ('patch', 'patch'))
    apiparamvalue = models.CharField('请求参数和值', max_length=800)  # 参数和值
    apimethod = models.CharField(
        verbose_name='请求方法',
        choices=REQUEST_METHOD,
        default='get',
        max_length=200,
        null=True)  # 请求方法
    apiresult = models.CharField('预期结果', max_length=200)  # 预期结果
    apiresponse = models.CharField('响应数据', max_length=5000, null=True)  # 响应数据
    apistatus = models.BooleanField('是否通过')  # 测试结果
    create_time = models.DateTimeField('创建时间', auto_now=True)  # 创建时间-自动获取当前时间

    def __str__(self):
        return self.apistep


class Apis(models.Model):
    Product = models.ForeignKey(
        'product.Product', on_delete=models.CASCADE, null=True)  # 关联产品id
    apiname = models.CharField('后端模块', max_length=100)  # 接口标题
    apiurl = models.CharField('url地址', max_length=200)  # 地址
    apitester = models.CharField('测试负责人', max_length=16, null=True)  # 执行人
    apistatus = models.BooleanField('是否通过')  # 测试结果
    create_time = models.DateTimeField(
        '创建时间', auto_now_add=True)  # 创建时间-自动获取当前时间
    update_time = models.DateTimeField('修改时间', auto_now=True)  # 创建时间-自动获取当前时间

    class Meta:
        verbose_name = 'API测试用例'
        verbose_name_plural = 'API测试用例'

    def __str__(self):
        return self.apiname


class Apiinfo(models.Model):
    api = models.ForeignKey(
        'Apis',
        on_delete=models.CASCADE,
        null=True,
    )
    # 接口标题
    apiname = models.CharField('接口名称', max_length=100, null=True)
    # 请求方法
    REQUEST_METHOD = (('get', 'get'), ('post', 'post'), ('put', 'put'),
                      ('delete', 'delete'), ('patch', 'patch'))
    apimethod = models.CharField(
        verbose_name='请求方法',
        choices=REQUEST_METHOD,
        default='get',
        max_length=200,
        null=True)
    # 地址
    apiurl = models.CharField('url地址', max_length=200, null=True)
    # 请求参数和值param
    apiparamvalue = models.CharField(
        '请求参数param', max_length=800, null=True, blank=True)
    # 请求数据JSON
    apijson = models.CharField(
        '请求数据json', max_length=800, null=True, blank=True)
    # 响应数据
    apiresponse = models.CharField(
        '响应数据json',
        max_length=5000,
        null=True,
    )
    # 测试结果
    apistatus = models.BooleanField('是否通过', null=True)
    # 创建时间-自动获取当前时间
    create_time = models.DateTimeField('创建时间', auto_now=True)

    def __str__(self):
        return self.apiname
