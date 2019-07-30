# -*- coding:utf-8 -*-
# @Desc : 
# @Author : Administrator
# @Date : 2019-07-29 17:13

import xadmin
from .models import BannerInfo,EmailVerifyCode
from xadmin import views

# 配置后台管理主题样式
class BaseXadminSetting(object):
    enable_themes = True
    use_bootswatch = True

# 配置后台管理系统名称
class CommXadminSetting(object):
    site_title = '谷粒后台管理系统'
    site_footer = '尚硅谷IT教育'
    menu_style = 'accordion'  # 左侧导航伸缩


class BannerInfoXadmin(object):
    list_display = ['image','url','add_time']
    search_fields = ['image', 'url']
    list_filter = ['image', 'url']

class EmailVerifyCodeXadmin(object):
    list_display = ['code', 'email', 'send_type','add_time']



# 模型类后台注册管理
xadmin.site.register(BannerInfo,BannerInfoXadmin)
xadmin.site.register(EmailVerifyCode,EmailVerifyCodeXadmin)

# 设置全局后台管理系统主题
xadmin.site.register(views.BaseAdminView,BaseXadminSetting)
# 设置全局后台管理系统名称
xadmin.site.register(views.CommAdminView,CommXadminSetting)
