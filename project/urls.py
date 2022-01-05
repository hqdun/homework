from django.urls import path, re_path
from . import views
 
app_name = 'project'
urlpatterns = [
 
    path('', views.index, name='index'),                    # 主页
    re_path(r'^register/$',views.register,name='register'),    # 注册
    re_path(r'^login/$', views.login, name='login'),        # 登录
    re_path(r'^user/(?P<pk>\d+)/profile/$', views.profile, name='profile'), # 信息显示
    re_path(r'^user/(?P<pk>\d+)/profile/update/$', views.profile_update, name='profile_update'),    # 信息更新
    re_path(r'^user/(?P<pk>\d+)/pwdchange/$', views.pwd_change, name='pwd_change'), # 密码更新
    re_path(r'^logout/$', views.logout, name='logout'), # 退出登录

    # 课程 增 删 查 改
    path('course/', views.CourseList.as_view(), name='course_list'),
    re_path(r'^user/(?P<pk>\d+)/course/$', views.CourseListSelf.as_view(), name='course_list_self'),  # 用户查看自己的课程
    re_path(r'^course/create/$',views.CourseCreate.as_view(), name='course_create'),       # 教师创建课程
    re_path(r'^course/(?P<pk>\d+)/$',views.CourseDetail.as_view(), name='course_detail'),       # 查看课程详情
    re_path(r'^course/(?P<pk>\d+)/update/$',views.CourseUpdate.as_view(), name='course_update'),       # 教师更新课程
    re_path(r'^course/(?P<pk>\d+)/delete$',views.CourseDelete.as_view(), name='course_delete'),       # 教师删除课程

    # project/urls.py
    re_path(r'^course/(?P<pk>\d+)/select$', views.course_select, name='course_select'), # 学生加入课程
    re_path(r'^course/(?P<pk>\d+)/cancel$', views.course_cancel, name='course_cancel'), # 学生退出课程

    # re_path(r'^course/(?P<pk>\d+)/list$', views.HomeworkList, name='homework_list'),  # 学生进入课程
    # re_path(r'^course/(?P<pk>\d+)/homework/publish/$', views.HomeworkListPublished, name='homework_list_published'),  # 教师进入课程
    # 教师发布作业 增 删 查 改
    re_path(r'^course/(?P<pk>\d+)/homework/create/$',views.HomeworkCreate.as_view(), name='homework_create'), # 创建作业
    re_path(r'^course/(?P<pkr>\d+)/homework/(?P<pk>\d+)/$',views.HomeworkDetail.as_view(), name='homework_detail'), # 作业详情
    re_path(r'^course/(?P<pkr>\d+)/homework/(?P<pk>\d+)/update/$',views.HomeworkUpdate.as_view(), name='homework_update'), # 更新作业
    re_path(r'^course/(?P<pkr>\d+)/homework/(?P<pk>\d+)/delete$',views.HomeworkDelete.as_view(), name='homework_delete'), # 删除作业
    re_path(r'^course/(?P<pk>\d+)/homework/draft/$', views.HomeworkListDraft.as_view(), name='homework_list_publishing'), # 待发布作业列表
    re_path(r'^course/(?P<pk>\d+)/homework/publish/$', views.HomeworkListPublished.as_view(), name='homework_list_published'), # 已发布作业列表
    re_path(r'^course/(?P<pkr>\d+)/homework/(?P<pk>\d+)/publish/$',views.homework_publish, name='homework_publish'), # 将草稿发布

    # 学生提交作业 增 删 查 改
    re_path(r'^course/(?P<pk>\d+)/list$', views.HomeworkList.as_view(), name='homework_list'), # 所有作业列表
    # re_path(r'^course/(?P<pkr>\d+)/homework/(?P<pk>\d+)/list$', views.HandinList.as_view(), name='handin_list'), # 所有作业列表
    re_path(r'^course/(?P<pk>\d+)/handin/list$', views.HandinListDone.as_view(), name='handin_list_done'), # 已提交的作业列表
    re_path(r'^course/(?P<pkr>\d+)/homework/(?P<pk>\d+)/handin/create/$',views.HandinCreate.as_view(), name='handin_create'), # 创建提交的作业
    re_path(r'^course/(?P<pka>\d+)/homework/(?P<pkr>\d+)/handin/(?P<pk>\d+)/$',views.HandinDetail.as_view(), name='handin_detail'), # 提交的作业详情
    re_path(r'^course/(?P<pka>\d+)/homework/(?P<pkr>\d+)/handin/(?P<pk>\d+)/update/$',views.HandinUpdate.as_view(), name='handin_update'), # 更新提交的作业
    re_path(r'^course/(?P<pka>\d+)/homework/(?P<pkr>\d+)/handin/(?P<pk>\d+)/delete/$',views.HandinDelete.as_view(), name='handin_delete'), # 删除提交的作业

    # 学生作业统计
    re_path(r'^course/(?P<pkr>\d+)/homework/(?P<pk>\d+)/count$', views.HomeworkHandin.as_view(), name='homework_handin_count'),
    # 学生统计
    re_path(r'^course/(?P<pk>\d+)/student$', views.course_student, name='course_student'),
    # 评论功能
    re_path(r'^comment/(?P<pk>[0-9]+)/$', views.homework_comment, name='homework_comment'),
    # 打分
    re_path(r'^handin/(?P<pk>\d+)/score$', views.score, name='score'),
    # 获取成绩
    path('get_score/', views.get_score, name='get_score'),
    #导出excel文件
    #path('export_excel/', views.export_excel, name='export_excel'),
    re_path(r'^course/(?P<pkr>\d+)/homework/(?P<pk>\d+)/export_excel$', views.export_excel,name='export_excel'),
    #机器人接口
    path('find_homework/', views.find_homework, name='find_homework'),
    path('teacher_homework/', views.teacher_homework, name='teacher_homework'),
]
