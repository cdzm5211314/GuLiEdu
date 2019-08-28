from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

# Create your models here.

"""
使用Django框架内部的AbstractUser模块扩展auth_user认证表:
1. 定义模型类继承from django.contrib.auth.models import AbstractUser
2. 扩展内置的auth_user表之后,一定要在settings.py中告诉Django,现在使用新定义的UserProfile表来做用户认证表
AUTH_USER_MODEL = "app应用名称.UserProfile"
# settings配置默认检查用户是否活跃状态is_axtive,不活跃返回None
# AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend']
# settings配置设置不检查用户的活跃状态is_active
# AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.AllowAllUsersModelBackend']
"""

# 用户表
class UserProfile(AbstractUser):
    image = models.ImageField(upload_to='user/',max_length=200,verbose_name='用户图像',null=True,blank=True)  # /static/media/user/
    nick_name = models.CharField(max_length=20,verbose_name="用户昵称",null=True,blank=True)
    birthday = models.DateField(verbose_name="用户生日",null=True,blank=True)
    gender = models.CharField(choices=(('girl','女'),('boy','男')),max_length=10,verbose_name="用户性别",default='girl')
    address = models.CharField(max_length=200,verbose_name="用户地址",null=True,blank=True)
    phone = models.CharField(max_length=11,verbose_name="用户手机",null=True,blank=True)
    # 这个字段控制激活
    is_start = models.BooleanField(default=False,verbose_name="是否激活")
    add_time = models.DateTimeField(default=datetime.now,verbose_name="添加时间")

    def __str__(self):
        return self.username

    def get_message_counter(self):  # 在用户模型类中定义方法,用来统计用户的未读消息个数
        from operations.models import UserMessage
        counter = UserMessage.objects.filter(message_man=self.id,message_status=False).count()  # 统计未读消息
        return counter

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name


# 轮播图表
class BannerInfo(models.Model):
    image = models.ImageField(upload_to='banner/',verbose_name="轮播图片",max_length=200)  # /static/media/banner/
    url = models.URLField(default='http://www.atguigu.com',max_length=200,verbose_name="图片链接")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return str(self.image)

    class Meta:
        verbose_name = '轮播图信息'
        verbose_name_plural = verbose_name

# 邮箱验证码
class EmailVerifyCode(models.Model):
    code = models.CharField(max_length=20,verbose_name="邮箱验证码")
    email = models.EmailField(max_length=200,verbose_name="验证码邮箱")
    send_type = models.IntegerField(choices=((1,'register'),(2,'forget'),(3,'change')),verbose_name="验证码类型")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = '邮箱验证码信息'
        verbose_name_plural = verbose_name