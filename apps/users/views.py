from django.shortcuts import render, redirect, reverse, HttpResponse
from users.forms import UserRegisterForm, UserLoginForm,UserForgetForm,UserResetForm,UserChangeimageForm,UserChangeInfoForm,UserChangeEmailForm,UserResetEmailForm
from users.models import UserProfile,EmailVerifyCode
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from tools.send_email_tool import send_mail_code
from django.http import JsonResponse
from datetime import datetime
from operations.models import UserLove,UserMessage
from orgs.models import OrgInfo,TeacherInfo
from courses.models import CourseInfo

# Create your views here.

# 主页
def index(request):
    return render(request, 'index.html')


# 注册
def user_register(request):
    if request.method == 'GET':
        # 此处实例化forms类,目的不是为了验证,而是为了使用验证码
        user_register_form = UserRegisterForm()
        return render(request, 'users/register.html',{'user_register_form':user_register_form})
    else:
        # 获取form注册表单数据
        user_register_form = UserRegisterForm(request.POST)
        if user_register_form.is_valid():  # 验证注册的邮箱与密码数据
            # 提取提交的数据
            email = user_register_form.cleaned_data['email']
            password = user_register_form.cleaned_data['password']
            # 到数据库查询注册的账号是否存在
            user_list = UserProfile.objects.filter(Q(username=email) | Q(email=email))
            if user_list:  # 注册的账号存在
                return render(request, 'users/register.html', {'mgs': '用户已经存在!!!'})
            else:  # 注册的账号不存在
                user = UserProfile()
                user.username = email
                user.set_password(password)
                user.email = email
                user.save()
                send_mail_code(email,1)
                return HttpResponse("请尽快登陆你的邮件进行账号激活,否则无法登陆...")
                # return redirect(reverse('index'))
        else:  # 表单数据验证不合法
            return render(request, 'users/register.html', {
                'user_register_form': user_register_form
            })


# 登陆
def user_login(request):
    if request.method == 'GET':
        return render(request, 'users/login.html')
    else:
        # 获取form登陆表单数据
        user_login_form = UserLoginForm(request.POST)
        if user_login_form.is_valid():  # 验证登陆的邮箱与密码数据
            # 验证成功,获取提交的数据
            email = user_login_form.cleaned_data['email']
            password = user_login_form.cleaned_data['password']
            # 验证用户信息,正确返回True
            user = authenticate(username=email, password=password)
            print(user)
            if user:
                # 判断用户是否被激活,如果没激活则无法登陆
                if user.is_start:  # 已激活
                    login(request,user)
                    # 登陆成功后发一条信息
                    userMessage = UserMessage()
                    userMessage.message_man = user.id
                    userMessage.message_content = '欢迎登陆...'
                    userMessage.save()

                    return redirect(reverse('index'))
                else:
                    return HttpResponse("你的账号未被激活,请去邮箱激活,否则无法登陆...")
            else:
                return render(request,'users/login.html',{'mgs':'用户名或密码错误'})
        else:
            return render(request,'users/login.html',{'user_login_form':user_login_form})

# 退出
def user_logout(request):
    logout(request)
    return redirect(reverse('index'))


# 注册账号激活
def user_active(request,code):
    if code:  # 获取到验证码参数
        emailVerifyCode_list = EmailVerifyCode.objects.filter(code=code)  # 根据验证码查找数据库是否存在数据
        if emailVerifyCode_list: # 数据库存在数据
            email = emailVerifyCode_list[0].email  # 获取到邮箱
            user_list = UserProfile.objects.filter(username=email)  # 根据邮箱查找用户信息数据
            if user_list:  # 数据库存在数据
                user = user_list[0]
                user.is_start = True  # 修改用户的激活字段is_start = True
                user.save()  # 注册账号已经激活
                return redirect(reverse('users:user_login'))  # 重定向到登陆页面
            else:
                pass
        else:
            pass
    else:
        pass

# 重置密码邮箱验证码
def user_forget(request):
    if request.method == "GET":
        # 此处实例化forms类,目的不是为了验证,而是为了使用验证码
        user_forget_form = UserForgetForm()
        return render(request,'users/forgetpwd.html',{'user_forget_form':user_forget_form})
    else:
        # 获取提交的form表单数据
        user_forget_form = UserForgetForm(request.POST)
        if user_forget_form.is_valid():  # 验证表单数据
            email = user_forget_form.cleaned_data['email']  # 获取账号信息
            user_list = UserProfile.objects.filter(email=email)  # 根据email到数据库查询用户信息
            if user_list:  # 用户存在
                send_mail_code(email,2)
                return HttpResponse("请登陆邮箱重置您的密码!!!")
            else:  # 用户不存在
                return render(request,'users/forgetpwd.html',{'msg':'用户不存在...'})
        else:  # 表单验证不通过
            return render(request,'users/forgetpwd.html',{'user_forget_form':user_forget_form})

# 重置密码
def user_reset(request,code):
    if code:  #  是否获取到验证码
        if request.method == 'GET':
            return render(request,'users/password_reset.html',{'code':code})
        else:  # post请求
            user_reset_form = UserResetForm(request.POST)
            if user_reset_form.is_valid():  # 验证数据
                password = user_reset_form.cleaned_data['password']
                password1 = user_reset_form.cleaned_data['password1']
                if password == password1:
                    emailVerifyCode_list = EmailVerifyCode.objects.filter(code=code)  # 根据验证码参数查询邮件验证码数据
                    if emailVerifyCode_list:  # 数据存在
                        email = emailVerifyCode_list[0].email  # 根据查询到的数据获取email信息
                        user_list = UserProfile.objects.filter(email=email)
                        if user_list:
                            user = user_list[0]
                            user.set_password(password)
                            user.save()
                            return redirect(reverse('users:user_login'))
                        else:  # 用户不存在
                            pass
                    else:  # 邮箱验证码数据不存在
                        pass
                else:
                    return render(request,'users/password_reset.html',{'msg':'两次密码输入不一致','code':code})
            else:  # form表单数据验证不通过
                return render(request,'users/password_reset.html',{'user_reset_form':user_reset_form,'code':code})
    else:  # 未获取到邮箱验证码
        pass

# 个人用户中心-个人资料
def user_info(requests):

    return render(requests,'users/usercenter-info.html')

# 个人用户中心-个人资料-修改用户头像
def user_changeimage(request):
    # request.POST 验证图片文件以外的其他内容
    # request.FILES 验证图片文件
    # instance 指明实例是什么,做修改的时候,我们需要知道给哪个对象实例进行修改
    # instance 如果不指明,就会当做创建对象去执行,而我们只有一个图片,就会报错
    user_changeimage_form = UserChangeimageForm(request.POST,request.FILES,instance=request.user)
    if user_changeimage_form.is_valid():
        user_changeimage_form.save(commit=True)
        return JsonResponse({'status':'ok'})
    else:
        return JsonResponse({'status':'fail'})

# 个人用户中心-个人资料-修改用户信息
def user_changeinfo(request):
    user_changeinfo_form = UserChangeInfoForm(request.POST,instance=request.user)
    if user_changeinfo_form.is_valid():
        user_changeinfo_form.save(commit=True)
        return JsonResponse({'status':'ok','msg':'修改成功'})
    else:
        return JsonResponse({'status':'fail','msg':'修改失败'})

# 个人用户中心-个人资料-修改用户邮箱-发送验证码
def user_changeemail(request):
    user_changeemail_form = UserChangeEmailForm(request.POST)
    if user_changeemail_form.is_valid():  # 验证输入的新邮箱数据
        email = user_changeemail_form.cleaned_data['email']  # 获取新邮箱

        email_list = UserProfile.objects.filter(Q(email=email)|Q(username=email))  # 查询新的邮箱是否在数据库表中
        if email_list:  # 说明这个新邮箱已在数据库中,则无法使用
            return JsonResponse({'status':'fail','msg':'此邮箱已被绑定'})
        else:  # 说明这个新邮箱不在数据库中,可以使用
            # 在发送邮件验证码之前,应该去邮箱验证码表中查找,看看之前有没有往当前这个新邮箱发送过修改邮箱这个类型的验证码
            email_ver_list = EmailVerifyCode.objects.filter(email=email,send_type=3)
            if email_ver_list:  # 说明发送过验证码,那么需要获取到新近发送这个一个验证码时间
                email_ver = email_ver_list.order_by('-add_time')[0]
                # 判断当前时间与最近发送的验证码添加时间之差
                if (datetime.now() - email_ver.add_time).seconds > 60:  # 表示距离上次发送验证码时间大于60秒,可以再次发送
                    send_mail_code(email,3)
                    # 如果我们重新发送了新的验证码,那么以前最近发的就可以清楚掉
                    email_ver.delete()
                    return JsonResponse({'status':'ok','msg':'请去你的新邮箱中获取验证码'})
                else:  # 小于60秒,不需要再次发送验证码
                    return JsonResponse({'status':'fail','msg':'请不要重发发送验证码,60秒后再试'})
            else:  # 未发送过验证码
                send_mail_code(email,3)
                return JsonResponse({'status':'ok','msg':'请去你的新邮箱中获取验证码'})
    else:  # 输入的邮箱信息未通过验证
        return JsonResponse({'status':'fail','msg':'输入邮箱信息错误'})

# 个人用户中心-个人资料-修改用户邮箱-完成
def user_resetemail(request):

    user_resetemail_form = UserResetEmailForm(request.POST)
    if user_resetemail_form.is_valid():
        email = user_resetemail_form.cleaned_data['email']
        code = user_resetemail_form.cleaned_data['code']

        email_ver_list = EmailVerifyCode.objects.filter(email=email,code=code,)  # 查找新邮箱与新邮箱验证码是否在数据表中存在这个对象
        if email_ver_list:
            email_ver = email_ver_list[0]
            if (datetime.now() - email_ver.add_time).seconds < 60:  # 说明验证码还未过期
                request.user.username = email
                request.user.email = email
                request.user.save()
                return JsonResponse({'status':'ok','msg':'新邮箱修改成功'})
            else:  # 大于60秒
                return JsonResponse({'status':'fail','msg':'验证码已过期,请重新发送验证码'})
        else:  # 未在数据库表中查找到数据
            return JsonResponse({'status':'fail','msg':'邮箱或验证码输入错误'})
    else:  # 数据未通过验证
        return JsonResponse({'status':'fail','msg':'邮箱或验证码不合法'})

# 个人用户中心-我的课程
def user_course(request):

    # 根据登陆用户信息 查找 用户课程表的数据
    usercourse_list = request.user.usercourse_set.all()
    # 在根据用户课程表 信息 获取到所有的 课程信息
    course_list = [usercourse.study_course for usercourse in usercourse_list]

    return render(request,'users/usercenter-mycourse.html',{
        'course_list':course_list,
    })

# 个人用户中心-我的收藏(机构1)
def user_loveorg(request):

    # 根据登陆用户查找 用户收藏表的所有信息  然后在根据 类型 筛选出收藏信息(机构)
    # userloveorg_list = request.user.userlove_set.all()
    # 直接从 用户收藏表 中根据登陆用户于类型字典  查找到需要的收藏信息(机构)
    userloveorg_list = UserLove.objects.filter(love_man=request.user,love_type=1,love_status=True)

    # 根据收藏信息获取到收藏id(机构)
    org_ids = [userloveorg.love_id for userloveorg in  userloveorg_list]

    # 根据收藏id查找到机构信息
    org_list = OrgInfo.objects.filter(id__in=org_ids)

    return render(request,'users/usercenter-fav-org.html',{
        'org_list':org_list,
    })

# 个人用户中心-我的收藏(讲师3)
def user_loveteacher(request):

    # 根据登陆用户查找 用户收藏表的所有信息  然后在根据 类型 筛选出收藏信息(讲师)
    # userloveteacher_list = request.user.userlove_set.all()
    # 直接从 用户收藏表 中根据登陆用户于类型字典  查找到需要的收藏信息(讲师)
    userloveteacher_list = UserLove.objects.filter(love_man=request.user,love_type=3,love_status=True)

    # 根据收藏信息获取到收藏id(讲师)
    teacher_ids = [userloveteacher.love_id for userloveteacher in  userloveteacher_list]

    # 根据收藏id查找到机构信息
    teacher_list = TeacherInfo.objects.filter(id__in=teacher_ids)

    return render(request,'users/usercenter-fav-teacher.html',{
        'teacher_list':teacher_list,
    })

# 个人用户中心-我的收藏(课程2)
def user_lovecourse(request):

    # 根据登陆用户查找 用户收藏表的所有信息  然后在根据 类型 筛选出收藏信息(课程)
    # userlovecourse_list = request.user.userlove_set.all()
    # 直接从 用户收藏表 中根据登陆用户于类型字典  查找到需要的收藏信息(课程)
    userlovecourse_list = UserLove.objects.filter(love_man=request.user,love_type=2,love_status=True)

    # 根据收藏信息获取到收藏id(课程)
    course_ids = [userlovecourse.love_id for userlovecourse in  userlovecourse_list]

    # 根据收藏id查找到机构信息
    course_list = CourseInfo.objects.filter(id__in=course_ids)

    return render(request,'users/usercenter-fav-course.html',{
        'course_list':course_list,
    })

# 个人用户中心-我的消息
def user_message(request):

    msg_list = UserMessage.objects.filter(message_man=request.user.id)

    return render(request,'users/usercenter-message.html',{
        'msg_list':msg_list,
    })

# 个人用户中心-我的消息-未读消息变成已读消息
def user_deletemessage(request):

    msgid = request.GET.get('msgid','')  # ajax请求传递过来未读消息的id
    if msgid:
        userMessage = UserMessage.objects.filter(id=int(msgid))[0]  # 根据消息id从消息表查找消息对象
        userMessage.message_status = True  # 修改未读消息的状态False(默认)为True
        userMessage.save()
        return JsonResponse({'status':'ok','msg':'已读'})
    else:
        return JsonResponse({'status':'fail','msg':'读取失败'})

