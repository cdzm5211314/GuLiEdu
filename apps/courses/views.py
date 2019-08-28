from django.shortcuts import render
from courses.models import CourseInfo
from operations.models import UserLove, UserCourse, UserComment
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q

# Create your views here.

# 公开课列表
def course_list(request):
    # 查询所有的公开课程
    all_courses = CourseInfo.objects.all().order_by('-add_time')
    # 查询公开课程中的推荐课程,根据最新推荐课程获取
    recommend_courses = all_courses.order_by('-add_time')[:3]

    # 全局搜索功能过滤
    keywords = request.GET.get('keywords','')
    if keywords:
        # 根据讲师名称模糊查找
        all_courses = all_courses.filter(Q(name__icontains = keywords)|Q(desc__icontains=keywords)|Q(detail__icontains=keywords))

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
        'keywords':keywords,
    })

# 公开课课程详情页
def course_detail(request, course_id):
    if course_id:
        # 根据id查询课程信息
        course = CourseInfo.objects.filter(id = int(course_id))[0]

        # 课程详情页访问一次 访问量+1
        course.click_num += 1
        course.save()

        # 根据类别查看相关课程信息
        relate_course = CourseInfo.objects.filter(category=course.category).exclude(id=int(course_id))[0]

        # lovecourse和loveorg 用来存储用户收藏这个东西的状态，在模板当中根据这个状态来确定页面加载时候，显示的是收藏还是取消收藏
        lovecourse = False  # 课程的收藏状态(页面显示)
        loveorg = False  # 机构的收藏状态(页面显示)
        if request.user.is_authenticated():  # 验证用户是否登录
            # 根据要课程id,课程类型,登录用户查询收藏表中是否存在这条记录
            love = UserLove.objects.filter(love_id=int(course_id),love_type=2,love_status=True,love_man=request.user)
            if love:
                lovecourse = True
            # 根据要机构id,机构类型,登录用户查询收藏表中是否存在这条记录
            love = UserLove.objects.filter(love_id=course.orginfo.id,love_type=1,love_status=True,love_man=request.user)
            if love:
                loveorg = True

        return render(request,'courses/course-detail.html',{
            'course': course,
            'relate_course':relate_course,
            'lovecourse': lovecourse,
            'loveorg': loveorg,
        })

# 公开课课程视频-章节
def course_video(request, course_id):
    if course_id:
        course = CourseInfo.objects.filter(id=int(course_id))[0]

        # 当用户点击我要"开始学习",代表会把这条记录添加到UserCourse表中
        userCourse_list = UserCourse.objects.filter(study_course=course, study_man=request.user)
        if not userCourse_list:  # 表示用户之前并未学习这个课程,也未添加到UserCourse表
            userCourse = UserCourse()
            userCourse.study_course = course
            userCourse.study_man = request.user
            userCourse.save()

            # 从学习课程表中查找该用户学习的所有课程
            usercourse_list = UserCourse.objects.filter(study_man=request.user)
            course_list = [usercourse.study_course for usercourse in usercourse_list]
            # 根据获取到课程列表,找到该课程所属机构
            org_list = list(set([course.orginfo for course in course_list]))
            # 当学习的该课程所属机构 不在 此人学习课程的所机构中, 则机构学习人数动态+1
            if course.orginfo not in org_list:
                course.orginfo.study_num += 1
                course.orginfo.save()

        # 学过该课程的用户还学过哪些课程???(指当前用户还是学习该课程的所有用户)
        # 1.从用户课程表(UserCourse)中查找到所有学习过该课程的 所有对象(用户课程)
        usercourse_list = UserCourse.objects.filter(study_course=course)
        # 2.根据查询得到的所有用户课程对象获取对应的用户信息列表
        user_list = [usercourse.study_man for usercourse in usercourse_list]
        # 3.根据获取到的用户信息列表查询用户学习的其他课程的 所有对象(用户课程)
        usercourse_list = UserCourse.objects.filter(study_man__in=user_list).exclude(study_course=course)
        # 4.从获取到的用户课程列表中获取所有课程列表
        course_list = list(set([usercourse.study_course for usercourse in usercourse_list]))

        return render(request,'courses/course-video.html',{
            'course': course,
            'course_list':course_list,
        })

# 公开课课程视频-评论
def course_comment(request, course_id):

    if course_id:
        # 查询要评论的课程
        course = CourseInfo.objects.filter(id=int(course_id))[0]
        # 根据课程查询该课程下的所有评论
        all_comment  = UserComment.objects.filter(comment_course=course).order_by('-add_time')

        # 学过该课程的用户还学过哪些课程???(指当前用户还是学习该课程的所有用户)
        # 1.从用户课程表(UserCourse)中查找到所有学习过该课程的 所有对象(用户课程)
        usercourse_list = UserCourse.objects.filter(study_course=course)
        # 2.根据查询得到的所有用户课程对象获取对应的用户信息列表
        user_list = [usercourse.study_man for usercourse in usercourse_list]
        # 3.根据获取到的用户信息列表查询用户学习的其他课程的 所有对象(用户课程)
        usercourse_list = UserCourse.objects.filter(study_man__in=user_list).exclude(study_course=course)
        # 4.从获取到的用户课程列表中获取所有课程列表
        course_list = list(set([usercourse.study_course for usercourse in usercourse_list]))

    return render(request,'courses/course-comment.html',{
        'course':course,
        'all_comment':all_comment,
        'course_list':course_list,
    })


