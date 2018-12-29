from django.urls import path
from apitest import apiviews

urlpatterns = [
    path('apitest_manage/', apiviews.apitest_manage, name='apitest_manage'),
    path('apistep_manage/', apiviews.apistep_manage, name='apistep_manage'),
    path('apis_manage/', apiviews.apis_manage, name='apis_manage'),
    path('apiinfos_manage/', apiviews.apiinfos_manage, name='apiinfos_manage'),
    path('test/', apiviews.test),
    path('apisearch/', apiviews.apitestsearch, name='apitestsearch'),
    path('apistepsearch/', apiviews.apistepsearch, name='apistepsearch'),
    path('apissearch/', apiviews.apissearch, name='apissearch'),
    path('test_report/', apiviews.test_report),
]
