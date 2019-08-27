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
    # 重置密码邮件验证码
    url(r'^user_forget/$', views.user_forget, name='user_forget'),
    # 重置密码
    url(r'^user_reset/(\w+)$', views.user_reset, name='user_reset'),

    # 个人用户中心-个人资料
    url(r'^user_info/$', views.user_info, name='user_info'),
    # 个人用户中心-修改用户头像
    url(r'^user_changeimage/$', views.user_changeimage, name='user_changeimage'),
    # 个人用户中心-修改用户信息
    url(r'^user_changeinfo/$', views.user_changeinfo, name='user_changeinfo'),
    # 个人用户中心-修改用户邮箱-发送验证码
    url(r'^user_changeemail/$', views.user_changeemail, name='user_changeemail'),
    # 个人用户中心-修改用户邮箱-完成
    url(r'^user_resetemail/$', views.user_resetemail, name='user_resetemail'),

]
