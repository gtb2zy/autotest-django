from django.urls import path
from user import userviews

urlpatterns = [
    path('login/', userviews.login),
    path('home/', userviews.home),
    path('left/', userviews.left),
    path('welcome/', userviews.welcome),
    path('logout/', userviews.logout)
]
