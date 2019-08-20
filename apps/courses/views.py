from django.shortcuts import render
from courses.models import CourseInfo
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# Create your views here.

# 公开课列表
def course_list(request):
    # 查询所有的公开课程
    all_courses = CourseInfo.objects.all().order_by('-add_time')
    # 查询公开课程中的推荐课程,根据最新推荐课程获取
    recommend_courses = all_courses.order_by('-add_time')[:3]

    # 课程按照(最新,最热门[点击量],参与人数)进行排序
    sort = request.GET.get('sort', '')
    if sort:
        all_courses = all_courses.order_by('-' + sort)

    # 课程列表分页
    page_num = request.GET.get('page_num', '')  # 获取url传递过来的页码数值,默认值为1,可自定义
    paginator = Paginator(all_courses, 6)  # 创建分页对象,设置每页显示几条数据
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

    return render(request, 'courses/course-list.html', {
        'all_courses': all_courses,
        'recommend_courses': recommend_courses,
        'pages': pages,
        'sort': sort,

    })

# 公开课课程详情页
def course_detail(request, course_id):
    if course_id:
        # 根据id查询课程信息
        course = CourseInfo.objects.filter(id = int(course_id))[0]
        # 根据类别查看相关课程信息
        relate_course = CourseInfo.objects.filter(category=course.category).exclude(id=int(course_id))[0]

        return render(request,'courses/course-detail.html',{
            'course': course,
            'relate_course':relate_course,
        })


