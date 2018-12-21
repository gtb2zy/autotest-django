from django.contrib import admin
from apitest.models import Apitest, Apistep, Apis, Apiinfo


# Register your models here.
class ApistepAdmin(admin.TabularInline):
    list_display = [
        'apiname', 'apiurl', 'apiparamvalue', 'apimethod', 'apiresult',
        'apistatus', 'create_time', 'id', 'apitest'
    ]
    model = Apistep
    extra = 1


class ApitestAdmin(admin.ModelAdmin):
    list_display = [
        'apitestname', 'apitestdesc', 'apitester', 'apitestresult',
        'create_time', 'id'
    ]
    inlines = [ApistepAdmin]


class ApiinfosAdmin(admin.TabularInline):
    model = Apiinfo
    extra = 1


class ApisAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'Product', 'apiname', 'apiurl', 'apitester', 'apistatus',
        'create_time'
    ]
    inlines = [ApiinfosAdmin]


admin.site.register(Apitest, ApitestAdmin)
admin.site.register(Apis, ApisAdmin)
admin.site.site_title = 'LONGSYS'
admin.site.site_header = '自动化测试平台'
