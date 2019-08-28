# -*- coding:utf-8 -*-
# @Desc : 自定义装饰器
# @Author : Administrator
# @Date : 2019-08-28 17:22

from django.shortcuts import redirect,reverse
from django.http import JsonResponse

def login_decorators(func):
    def wrapper(request,*args,**kwargs):
        if request.user.is_authenticated():  # 验证用户是否登录
            return func(request,*args,**kwargs)
        else:  # 未登陆
            if request.is_ajax():  # 判断是否发送的是ajax请求
                return JsonResponse({'status':'nologin'})  # 未登录信息
            # 获取未登录前访问的完整url,并不单单只是路径
            url = request.get_full_path()
            result = redirect(reverse('users:user_login'))
            result.set_cookie('url',url)
            return result
    return wrapper


