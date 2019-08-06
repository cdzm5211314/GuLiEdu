# -*- coding:utf-8 -*-
# @Desc : 
# @Author : Administrator
# @Date : 2019-08-06 14:38

from django import forms
from operations.models import UserAsk
import re

# 我要学习的ajax请求咨询form表单: 使用model模型类的字段验证规则
# form表单与model模型的结合体django.forms.ModelForm
class UserAskForm(forms.ModelForm):
    # 使用model模型类的字段验证规则
    class Meta:
        model = UserAsk
        # 1.使用模型类的部分字段
        fields = ['name','phone','course']
        # 2.使用模型类的所有字段
        # fields = "__all__"
        # 3.除了模型类的某些字段外,其他所有字段都使用
        # exclude = ['add_time']

    # 使用model模型类的字段验证规则后再次使用自定义验证规则验证手机号码
    def clean_phone(self):
        phone = self.cleaned_data['phone']  # 从上诉的验证数据中获取字段再次自定义验证
        regex = re.compile('^1([358][0-9]|4[579]|66|7[0135678]|9[89])[0-9]{8}$')  # 正则匹配规则
        if regex.match(phone):  # 匹配成功
            return phone
        else:  # 匹配失败
            raise forms.ValidationError('手机号码不合法')





