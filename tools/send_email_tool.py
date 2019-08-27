# -*- coding:utf-8 -*-
# @Desc : 
# @Author : Administrator
# @Date : 2019-07-31 15:54

from django.core.mail import send_mail
from django.conf import settings
import string
import random
from users.models import EmailVerifyCode


# 生成验证码(随机字符串)
def get_random_code(slen):
    return ''.join(random.sample(string.ascii_letters + string.digits, slen))

# 发送验证码邮件
def send_mail_code(email,send_type):
    ## 1.创建邮箱验证码对象,保存数据,用以后作对比
    emailVerifyCode = EmailVerifyCode()
    emailVerifyCode.email = email
    emailVerifyCode.send_type = send_type
    # 获取验证码
    code = get_random_code(8)
    emailVerifyCode.code = code
    emailVerifyCode.save()

    ## 2.settings.py配置信息
    # EMAIL_HOST = 'smtp.163.com'                      # smpt服务地址
    # EMAIL_PORT = 25                                  # 端口号
    # EMAIL_HOST_USER = 'configureadmin@163.com'       # 发送邮件的邮箱地址即发件人
    # EMAIL_HOST_PASSWORD = 'asdfghjkl******'          # 发送邮件的邮箱[即发件人]中设置的客户端授权密码
    # EMAIL_FROM = '谷粒教育<configureadmin@163.com>'  # 收件人看到的发件人

    ## 3.发送邮件的具体内容信息
    # 激活用户
    if send_type == 1:
        send_title = "欢迎注册谷粒教育网站:"
        send_body = "请点击以下链接,进行激活账号: \n http://127.0.0.1:8000/users/user_active/" + code
        # 发送邮件
        send_mail(send_title,send_body,settings.EMAIL_FROM,[email])

    # 重置密码
    if send_type == 2:
        send_title = "谷粒教育重置密码系统:"
        send_body = "请点击以下链接,进行重置密码: \n http://127.0.0.1:8000/users/user_reset/" + code
        # 发送邮件
        send_mail(send_title,send_body,settings.EMAIL_FROM,[email])

    # 修改邮箱-获取验证码
    if send_type == 3:
        send_title = "谷粒教育重置邮箱验证码:"
        send_body = "你的邮箱验证码是: " + code
        # 发送邮件
        send_mail(send_title,send_body,settings.EMAIL_FROM,[email])

