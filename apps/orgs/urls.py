from django.conf.urls import url
from orgs import views

urlpatterns = [

    # 机构列表
    url(r'^org_list/$', views.org_list, name='org_list'),
    # 机构详情页-机构首页
    url(r'^org_detail/(\d+)/$', views.org_detail, name='org_detail'),
    # 机构详情页-机构课程
    url(r'^org_detail_course/(\d+)/$', views.org_detail_course, name='org_detail_course'),
    # 机构详情页-机构介绍
    url(r'^org_detail_desc/(\d+)/$', views.org_detail_desc, name='org_detail_desc'),
    # 机构详情页-机构讲师
    url(r'^org_detail_teacher/(\d+)/$', views.org_detail_teacher, name='org_detail_teacher'),

    # 讲师列表
    url(r'^teacher_list/$', views.teacher_list, name='teacher_list'),

]
