from django.conf.urls import url
from operations import views

urlpatterns = [
    # 我要学习的ajax请求咨询
    url(r'^user_ask/$', views.user_ask, name='user_ask'),

]
