from django.shortcuts import render
from orgs.models import OrgInfo,TeacherInfo,CityInfo

# Create your views here.

# 机构列表
def org_list(request):
    all_orgs = OrgInfo.objects.all()  # 查询所有的机构信息
    all_citys = CityInfo.objects.all()  # # 查询所有的城市信息
    sort_orgs = all_orgs.order_by('-love_num')[:3]  # 按照收藏数降序排序机构并获取收藏数最高的三个机构
    return render(request,'org-list.html',{
        'all_orgs':all_orgs,
        'all_citys':all_citys,
        'sort_orgs':sort_orgs,
    })


