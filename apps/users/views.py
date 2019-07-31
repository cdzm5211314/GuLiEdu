from django.shortcuts import render, redirect, reverse, HttpResponse
from .forms import UserRegisterForm, UserLoginForm
from users.models import UserProfile
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from tools.send_email_tool import send_mail_code

# Create your views here.

# 主页
def index(request):
    return render(request, 'index.html')


# 注册
def user_register(request):
    if request.method == 'GET':
        # 此处实例化forms类,目的不是为了验证,而是为了使用验证码
        user_register_form = UserRegisterForm()
        return render(request, 'register.html',{'user_register_form':user_register_form})
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
                return render(request, 'register.html', {'mgs': '用户已经存在!!!'})
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
            return render(request, 'register.html', {
                'user_register_form': user_register_form
            })


# 登陆
def user_login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
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
                    return redirect(reverse('index'))
                else:
                    return HttpResponse("你的账号未被激活,请去邮箱激活,否则无法登陆...")
            else:
                return render(request,'login.html',{'mgs':'用户名或密码错误'})
        else:
            return render(request,'login.html',{'user_login_form':user_login_form})

# 退出
def user_logout(request):
    logout(request)
    return redirect(reverse('index'))



