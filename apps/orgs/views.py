from django.shortcuts import render
from orgs.models import OrgInfo,TeacherInfo,CityInfo
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

# Create your views here.

# 机构列表
def org_list(request):
    all_orgs = OrgInfo.objects.all()  # 查询所有的机构信息
    all_citys = CityInfo.objects.all()  # 查询所有的城市信息
    sort_orgs = all_orgs.order_by('-love_num')[:3]  # 按照收藏数降序排序机构并获取收藏数最高的三个机构

    # 根据机构类别进行筛选过滤
    cate = request.GET.get('cate','')
    if cate:
        all_orgs = all_orgs.filter(category=cate)

    # 根据所在地区进行筛选过滤
    cityid = request.GET.get('cityid','')
    if cityid:
        all_orgs = all_orgs.filter(cityinfo_id=int(cityid))

    # 排序,根据学习人数或课程数进行排序
    sort = request.GET.get('sort','')
    if sort:
        all_orgs = all_orgs.order_by('-' + sort)


    # 分页显示
    page_num = request.GET.get('page_num','')  # 获取url传递过来的页码数值,默认值为1,可自定义
    paginator = Paginator(all_orgs,3)  # 创建分页对象,设置每页显示几条数据
    try:
        pages = paginator.page(page_num)  # 获取页码值对应的分页对象
    except PageNotAnInteger:  # 页码不是整数时引发该异常
        pages = paginator.page(1)  # 获取第一页数据返回
    except EmptyPage:  # 页码不在有效范围时(即数据为空,或参数页码值大于或小于页码范围)引发该异常
        # pages = paginator.page(paginator.num_pages)
        if int(page_num) > paginator.num_pages:
            # 参数页码值大于总页码数: 获取最后一页数据返回
            pages = paginator.page(paginator.num_pages)
        else:
            # 参数页码值小于最小页码数或为空时: 获取第一页数据返回
            pages = paginator.page(1)


    return render(request,'org-list.html',{
        'all_orgs':all_orgs,
        'pages':pages,
        'all_citys':all_citys,
        'sort_orgs':sort_orgs,
        'cate':cate,
        'cityid':cityid,
        'sort':sort,
    })


