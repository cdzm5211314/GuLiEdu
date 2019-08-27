# -*- coding:utf-8 -*-
# @Desc :
# @Author : Administrator
# @Date : 2019-07-30 17:01

from django import forms
from captcha.fields import CaptchaField
from users.models import UserProfile

# 注册表单类
class UserRegisterForm(forms.Form):
    email = forms.EmailField(required=True,error_messages={
        'required':'邮箱必须填写'
    })
    password = forms.CharField(required=True,min_length=6,error_messages={
        'required':'密码必须填写',
        'min_length':'密码至少6位'
    })

    captcha = CaptchaField()  # 验证码

# 登陆表单类
class UserLoginForm(forms.Form):
    email = forms.EmailField(required=True,error_messages={
        'required':'邮箱必须填写'
    })
    password = forms.CharField(required=True,min_length=6,error_messages={
        'required':'密码必须填写',
        'min_length':'密码至少6位'
    })

# 重置密码邮箱验证码表单
class UserForgetForm(forms.Form):
    email = forms.EmailField(required=True,error_messages={
        'required':'邮箱必须填写'
    })
    captcha = CaptchaField()  # 验证码

# 重置密码表单
class UserResetForm(forms.Form):
    password = forms.CharField(required=True,min_length=6,error_messages={
        'required':'密码必须填写',
        'min_length':'密码至少6位',
        'max_length':'密码不能超过20位',
    })
    password1 = forms.CharField(required=True,min_length=6,error_messages={
        'required':'密码必须填写',
        'min_length':'密码至少6位',
        'max_length':'密码不能超过20位',
    })

# 个人用户中心-修改用户头像
class UserChangeimageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']

# 个人用户中心-修改用户信息
class UserChangeInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name','birthday','gender','address','phone']

# 个人用户中心-修改用户邮箱-获取验证码
class UserChangeEmailForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['email']

