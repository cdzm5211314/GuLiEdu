from django.shortcuts import render
from operations.forms import UserAskForm
from django.http import JsonResponse


# Create your views here.

# 我要学习的ajax请求咨询
def user_ask(request):
    user_ask_form = UserAskForm(request.POST)
    if user_ask_form.is_valid():  # 数据验证通过
        user_ask_form.save(commit=True)
        return JsonResponse({'status': 'ok', 'msg': '咨询成功!!!'})
    else:
        return JsonResponse({'status': 'fail', 'msg': '咨询失败!!!'})
