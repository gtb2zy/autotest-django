from django.urls import path
from user import userviews

urlpatterns = [
    path('login/', userviews.login, name='login'),
    path('home/', userviews.home, name='home'),
    path('logout/', userviews.logout, name='logout')
]
