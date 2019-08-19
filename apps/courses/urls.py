from django.conf.urls import url
from courses import views

urlpatterns = [
    # 公开课列表
    url(r'^course_list/$',views.course_list, name='course_list'),

]
