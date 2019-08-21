from django.conf.urls import url
from courses import views

urlpatterns = [
    # 公开课列表
    url(r'^course_list/$',views.course_list, name='course_list'),
    # 公开课课程详情
    url(r'^course_detail/(\d+)/$',views.course_detail, name='course_detail'),
    # 公开课课程视频-章节
    url(r'^course_video/(\d+)/$',views.course_video, name='course_video'),
    # 公开课课程视频-评论
    url(r'^course_comment/(\d+)/$',views.course_comment, name='course_comment'),
]
