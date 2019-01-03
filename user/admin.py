from django.contrib import admin
from .models import LoginRecord


# Register your models here.
@admin.register(LoginRecord)
class LoginRecordAdmin(admin.ModelAdmin):
    list_display = [
        'login_num',
        'login_time',
    ]
