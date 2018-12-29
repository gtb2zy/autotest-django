from django.urls import path
from product import proviews

urlpatterns = [
    path('product_manage/', proviews.product_manage, name='product_manage'),
    path('prosearch/', proviews.prosearch, name='prosearch'),
]
