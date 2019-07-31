from django.conf.urls import url
from users import views


urlpatterns = [

    # 注册
    url(r'^user_register/$', views.user_register, name='user_register'),
    # 登陆
    url(r'^user_login/$', views.user_login, name='user_login'),
    # 退出
    url(r'^user_logout/$', views.user_logout, name='user_logout'),
    # 注册账号激活
    url(r'^user_active/(\w+)$', views.user_active, name='user_active'),

]
