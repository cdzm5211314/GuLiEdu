from django.conf.urls import url
from courses import views

urlpatterns = [
    # 公开课列表
    url(r'^course_list/$',views.course_list, name='course_list'),
    # 公开课课程详情
    url(r'^course_detail/(\d+)/$',views.course_detail, name='course_detail'),

]
