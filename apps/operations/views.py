from django.shortcuts import render
from operations.forms import UserAskForm
from operations.models import UserLove
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

# 机构收藏类型功能
def user_love(request):
    # 获取ajax请求参数
    loveid = request.GET.get('loveid','')
    lovetype = request.GET.get('lovetype','')
    # print(loveid,lovetype)
    if loveid and lovetype:  # 如果收藏id和收藏类型参数同时存在,首先去收藏表中查询有没有这个用户的收藏记录
        love = UserLove.objects.filter(love_id=int(loveid), love_type=int(lovetype),love_man=request.user)
        # print(love)
        if love:  # 在收藏表中存在这个用户的收藏记录
            # 判断这条收藏记录的状态
            if love[0].love_status:
                # 状态为真,表示之前收藏过,页面上显示为取消收藏,这次点击表示为取消收藏
                love[0].love_status = False
                love[0].save()
                return JsonResponse({'status':'ok', 'msg':'收藏'})
            else:  # 状态为假,表示之前收藏过,并且取消了,页面上显示为收藏,这次点击表示收藏
                love[0].love_status = True
                love[0].save()
                return JsonResponse({'status':'ok', 'msg':'取消收藏'})
        else:  # 在收藏表中不存在这个用户的收藏记录
            userLove = UserLove()
            userLove.love_id = int(loveid)
            userLove.love_type = int(lovetype)
            userLove.love_man = request.user
            userLove.love_status = True
            userLove.save()
            return JsonResponse({'status':'ok', 'msg':'取消收藏'})
    else:  # 收藏id和收藏类型参数不存在
        return JsonResponse({'status':'fail', 'msg':'收藏失败'})



