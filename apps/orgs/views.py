from django.shortcuts import render
from orgs.models import OrgInfo, TeacherInfo, CityInfo
from operations.models import UserLove
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# Create your views here.

# 机构列表
def org_list(request):
    all_orgs = OrgInfo.objects.all().order_by("id")  # 查询所有的机构信息
    all_citys = CityInfo.objects.all()  # 查询所有的城市信息
    sort_orgs = all_orgs.order_by('-love_num')[:3]  # 按照收藏数降序排序机构并获取收藏数最高的三个机构

    # 根据机构类别进行筛选过滤
    cate = request.GET.get('cate', '')
    if cate:
        all_orgs = all_orgs.filter(category=cate)

    # 根据所在地区进行筛选过滤
    cityid = request.GET.get('cityid', '')
    if cityid:
        all_orgs = all_orgs.filter(cityinfo_id=int(cityid))

    # 排序,根据学习人数或课程数进行排序
    sort = request.GET.get('sort', '')
    if sort:
        all_orgs = all_orgs.order_by('-' + sort)

    # 分页显示
    page_num = request.GET.get('page_num', '')  # 获取url传递过来的页码数值,默认值为1,可自定义
    paginator = Paginator(all_orgs, 3)  # 创建分页对象,设置每页显示几条数据
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

    return render(request, 'orgs/org-list.html', {
        'all_orgs': all_orgs,
        'pages': pages,
        'all_citys': all_citys,
        'sort_orgs': sort_orgs,
        'cate': cate,
        'cityid': cityid,
        'sort': sort,
    })


# 机构详情页-机构首页
def org_detail(request, org_id):
    if org_id:
        org = OrgInfo.objects.filter(id=int(org_id))[0]
        # 返回数据的时候需要返回收藏这个机构的状态(收藏或取消收藏)
        lovestatus = False
        if request.user.is_authenticated():  # 判断用户是否登录
            # 查看收藏表中是否有这条收藏记录数据
            love = UserLove.objects.filter(love_man=request.user, love_id=int(org_id), love_type=1, love_status=True)
            if love:
                lovestatus = True  # 机构页面显示为取消收藏

        return render(request, 'orgs/org-detail-homepage.html', {
            'org': org,
            'detail_type': 'home',
            'lovestatus': lovestatus,
        })


# 机构详情页-机构课程
def org_detail_course(request, org_id):
    if org_id:
        org = OrgInfo.objects.filter(id=int(org_id))[0]  # 根据id查询机构信息
        # 根据机构信息对象 查所有 它下面所有的课程
        all_orgs_course = org.courseinfo_set.all().order_by('id')  # order_by避免报分页警告信息

        # 返回数据的时候需要返回收藏这个机构的状态(收藏或取消收藏)
        lovestatus = False
        if request.user.is_authenticated():  # 判断用户是否登录
            # 查看收藏表中是否有这条收藏记录数据
            love = UserLove.objects.filter(love_man=request.user, love_id=int(org_id), love_type=1, love_status=True)
            if love:
                lovestatus = True  # 机构页面显示为取消收藏

        # 分页显示
        page_num = request.GET.get('page_num', '')  # 获取url传递过来的页码数值,默认值为1,可自定义
        paginator = Paginator(all_orgs_course, 4)  # 创建分页对象,设置每页显示几条数据
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

        return render(request, 'orgs/org-detail-course.html', {
            'org': org,
            'pages': pages,
            'detail_type': 'course',
            'lovestatus': lovestatus,
        })


# 机构详情页-机构介绍
def org_detail_desc(request, org_id):
    if org_id:
        org = OrgInfo.objects.filter(id=int(org_id))[0]

        # 返回数据的时候需要返回收藏这个机构的状态(收藏或取消收藏)
        lovestatus = False
        if request.user.is_authenticated():  # 判断用户是否登录
            # 查看收藏表中是否有这条收藏记录数据
            love = UserLove.objects.filter(love_man=request.user, love_id=int(org_id), love_type=1, love_status=True)
            if love:
                lovestatus = True  # 机构页面显示为取消收藏

        return render(request, 'orgs/org-detail-desc.html', {
            'org': org,
            'detail_type': 'desc',
            'lovestatus': lovestatus,
        })


# 机构详情页-机构讲师
def org_detail_teacher(request, org_id):
    if org_id:
        org = OrgInfo.objects.filter(id=int(org_id))[0]
        # print(org,type(org))

        # 返回数据的时候需要返回收藏这个机构的状态(收藏或取消收藏)
        lovestatus = False
        if request.user.is_authenticated():  # 判断用户是否登录
            # 查看收藏表中是否有这条收藏记录数据
            love = UserLove.objects.filter(love_man=request.user, love_id=int(org_id), love_type=1, love_status=True)
            if love:
                lovestatus = True  # 机构页面显示为取消收藏

        return render(request, 'orgs/org-detail-teachers.html', {
            'org': org,
            'detail_type': 'teacher',
            'lovestatus': lovestatus,
        })

# 讲师列表
def teacher_list(request):

    # 查询所有讲师
    all_teachers = TeacherInfo.objects.all().order_by('id')

    # 排序-默认(id)和人气(点击量click_num)
    sort = request.GET.get('sort','')
    if sort:
        all_teachers = all_teachers.order_by('-' + sort)

    # 讲师分页
    page_num = request.GET.get('page_num', '')  # 获取url传递过来的页码数值,默认值为1,可自定义
    paginator = Paginator(all_teachers, 3)  # 创建分页对象,设置每页显示几条数据
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

    # 讲师排行榜-根据点击量(click_num)或收藏量(love_num)排序
    sort_teacher = all_teachers.order_by('-love_num')[:3]

    return render(request,'orgs/teachers-list.html',{
        'all_teachers':all_teachers,
        'pages':pages,
        'sort':sort,
        'sort_teacher':sort_teacher,
    })