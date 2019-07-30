# -*- coding:utf-8 -*-
# @Desc :
# @Author : Administrator
# @Date : 2019-07-30 9:20

import xadmin
from .models import *

# Create your models here.
class CourseInfoXadmin(object):
    list_display = ['image','name','study_num','level','love_num','category','orginfo','teacherinfo']
    model_icon = 'fa fa-cogs'  # 修改xadmin后台左侧栏图标样式

class LessonInfoXadmin(object):
    list_display = ['name', 'courseinfo', 'add_time']


class VideoInfoXadmin(object):
    list_display = ['name', 'study_time', 'url','lessoninfo']


class SourceInfoXadmin(object):
    list_display = ['name', 'down_load', 'courseinfo', 'add_time']



xadmin.site.register(CourseInfo,CourseInfoXadmin)
xadmin.site.register(LessonInfo,LessonInfoXadmin)
xadmin.site.register(VideoInfo,VideoInfoXadmin)
xadmin.site.register(SourceInfo,SourceInfoXadmin)