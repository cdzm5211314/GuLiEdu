from django.conf.urls import url
from operations import views

urlpatterns = [
    # 我要学习的ajax请求咨询
    url(r'^user_ask/$', views.user_ask, name='user_ask'),
    # 收藏类型功能
    url(r'^user_love/$',views.user_love, name='user_love'),
    # 取消收藏类型功能
    url(r'^user_deletelove/$',views.user_deletelove, name='user_deletelove'),
    # 用户评论
    url(r'^user_comment/$',views.user_comment, name='user_comment'),
]
