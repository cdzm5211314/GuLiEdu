from django.conf.urls import url
from orgs import views

urlpatterns = [

    # 机构列表
    url(r'^org_list/$', views.org_list, name='org_list'),
    # 机构详情页
    url(r'^org_detail/(\d+)/$', views.org_detail, name='org_detail'),

]
