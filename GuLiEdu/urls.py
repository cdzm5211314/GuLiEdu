"""GuLiEdu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
# from django.contrib import admin
import xadmin
from apps.users import views
from users.views import IndexView

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    # 使用xadmin插件
    url(r'^xadmin/', xadmin.site.urls),
    # 使用验证码
    url(r'^captcha/',include('captcha.urls')),
    # 使用DjangoUeditor富文本插件
    url(r'^ueditor/',include('DjangoUeditor.urls')),

    # 路由分发
    url(r'^users/', include('users.urls', namespace='users')),
    url(r'^courses/', include('courses.urls', namespace='courses')),
    url(r'^orgs/', include('orgs.urls', namespace='orgs')),
    url(r'^operations/', include('operations.urls', namespace='operations')),

    # 主页 --- FBV
    # url(r'^$', views.index, name='index'),
    # 主页 --- CBV
    url(r'^$', IndexView.as_view(), name='index'),

]
