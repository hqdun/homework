from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Teacher,Student,Role,Course, Homework, Handin
from .forms import RegistrationForm, LoginForm, StudentProfileForm,TeacherProfileForm, PwdChangeForm, CourseForm, HomeworkForm, HandinForm, CommentForm
from django.urls import reverse, reverse_lazy #reverse url别名反向解析
from django.http import HttpResponseRedirect, Http404, HttpResponse

from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
import datetime
import xlwt
def index(request):
    return render(request,'project/index.html')

 #注册
def register(request):
    if request.method == 'POST':
        # 验证表单RegistrationForm的数据是否有效
        form = RegistrationForm(request.POST)
        print(form)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password2']
            email = form.cleaned_data['email']
            role = form.cleaned_data['role']
            # 使用内置User自带create_user方法创建用户，不需要使用save()
            user = User.objects.create_user(username=username, password=password,email=email)
            # 首先创建一个 Role，然后 Student 或 Teacher 一对一绑定该 Role
            role_profile = Role(role=int(role),user=user)
            role_profile.save()
            # 如果直接使用objects.create()方法后不需要使用save()
            if int(role) == 0:
                user_profile = Student(user=role_profile)
                user_profile.save()
            else:
                user_profile = Teacher(user=role_profile)
                user_profile.save()
            #  注册成功，通过HttpResponseRedirect方法转到登录页面
            return HttpResponseRedirect("/login/")
    else:
        # 如果用户没有提交表单或不是通过POST方法提交表单，转到登录页面，
        # 生成一张空的 RegistrationForm
        form = RegistrationForm()
    return render(request, 'project/register.html', {'form': form})

 #登录
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        # print(form)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # 调用Django自带的auth.authenticate() 来验证用户名和密码是否正确
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
            	# 调用auth.login()来进行登录
                auth.login(request, user)
                # 登录成功，转到用户个人信息页面
                # []是有序的可reverse，{}是无序的
                return HttpResponseRedirect(reverse('project:index'))
            else:
                # 登录失败
                return render(request, 'project/login.html', {'form': form,'message': '密码错误，请重试！'})
    else:
    	# 如果用户没有提交表单或不是通过POST方法提交表单，转到登录页面，生成一张空的LoginForm
        form = LoginForm()
    return render(request, 'project/login.html', {'form': form})

#退出登录
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/login/")

#个人信息
def profile(request,pk):
    user = get_object_or_404(User,pk=pk)
    return render(request,'project/profile.html',{'user':user})

#信息更新
# def profile_update(request, pk):
#     user = get_object_or_404(User, pk=pk)
#     if request.method == "POST":
#         form = ProfileForm(request.POST)
#         if form.is_valid():
#             if request.user.role.role == 0:
#                 user.role.student.name = form.cleaned_data['name']
#                 user.role.student.gender = form.cleaned_data['gender']
#                 user.role.student.description = form.cleaned_data['description']
#                 user.role.student.save()
#                 user.email = form.cleaned_data['email']
#                 user.save()
#                 # 请重新复习一遍 URL 重定向的三种方法
#                 return HttpResponseRedirect(reverse('project:profile', args=[user.id]))
#             else:
#                 user.role.teacher.name = form.cleaned_data['name']
#                 user.role.teacher.gender = form.cleaned_data['gender']
#                 user.role.teacher.description = form.cleaned_data['description']
#                 user.role.teacher.save()
#                 user.email = form.cleaned_data['email']
#                 user.save()
#                 return HttpResponseRedirect(reverse('project:profile', args=[user.id]))
#     else:
#         if request.user.role.role == 0:
#             default_data = {'name': user.role.student.name,
#                             'gender': user.role.student.gender,
#                             'description':  user.role.student.description,
#                             'email' : user.email,
#                         }
#         else:
#             default_data = {'name': user.role.teacher.name,
#                             'gender': user.role.teacher.gender,
#                             'description': user.role.teacher.description,
#                             'email': user.email,
#                         }
#         form = ProfileForm(default_data)
#     return render(request, 'project/profile_update.html', {'form': form, 'user': user})

#信息更新
def profile_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.user.role.role == 0:
        if request.method == "POST":
            form = StudentProfileForm(request.POST)
            if form.is_valid():
                user.role.student.name = form.cleaned_data['name']
                user.role.student.gender = form.cleaned_data['gender']
                user.role.student.classes = form.cleaned_data['classes']
                user.role.student.description = form.cleaned_data['description']
                user.role.student.save()
                user.email = form.cleaned_data['email']
                user.save()
                # 请重新复习一遍 URL 重定向的三种方法
                return HttpResponseRedirect(reverse('project:profile', args=[user.id]))
        else:
             default_data = {'name': user.role.student.name,
                             'gender': user.role.student.gender,
                             'description': user.role.student.description,
                             'email': user.email,
                             'classes' : user.role.student.classes,
                             }
        form = StudentProfileForm(default_data)
    else:
        if request.method == "POST":
            form = TeacherProfileForm(request.POST)
            if form.is_valid():
                user.role.teacher.name = form.cleaned_data['name']
                user.role.teacher.gender = form.cleaned_data['gender']
                user.role.teacher.ranks = form.cleaned_data['ranks']
                user.role.teacher.description = form.cleaned_data['description']
                user.role.teacher.save()
                user.email = form.cleaned_data['email']
                user.save()
                # 请重新复习一遍 URL 重定向的三种方法
                return HttpResponseRedirect(reverse('project:profile', args=[user.id]))
        else:
            default_data = {'name': user.role.teacher.name,
                            'gender': user.role.teacher.gender,
                            'description': user.role.teacher.description,
                            'email': user.email,
                            'ranks' : user.role.teacher.ranks,
                            }
        form = TeacherProfileForm(default_data)

    return render(request, 'project/profile_update.html', {'form': form, 'user': user})


#密码修改
def pwd_change(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        form = PwdChangeForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['old_password']
            username = user.username
            # auth.authenticate 对用户登录的账号密码进行验证，若通过验证，则返回 None
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                new_password = form.cleaned_data['password2']
                user.set_password(new_password)
                user.save()
                return HttpResponseRedirect("/login/")
            else:
                return render(request, 'project/pwd_change.html', {'form': form,'user': user, 'message': '原密码错误，请重新输入！'})
    else:
        form = PwdChangeForm()
    return render(request, 'project/pwd_change.html', {'form': form, 'user': user})

# 所有课程列表
class CourseList(ListView):
    template_name = 'project/course_list.html'
    def get_queryset(self):
        return Course.objects.all().order_by("id")
# 用户课程列表
class CourseListSelf(ListView):
    template_name = 'project/course_list_self.html' # 指定这个列表的模板。
    def get_queryset(self):
        # 根据用户角色来返回相应数据
        if self.request.user.role.role == 1:
            return Course.objects.filter(teacher=self.request.user.role.teacher).order_by("id")
        else:
            return Course.objects.filter(student=self.request.user.role.student).order_by("id")

class CourseDetail(DetailView):
    model = Course
    template_name = 'project/course_detail.html'

# 创建课程的视图类
class CourseCreate(CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'project/course_form.html'
    # 将创建对象的用户与 model 里的 user 结合
    def form_valid(self,form):
        form.instance.teacher = self.request.user.role.teacher
        return super().form_valid(form)

# 更新课程
class CourseUpdate(UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'project/course_form.html'
    # 只有创建该课程的教师才可以更新该课程
    def get_object(self,queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.teacher != self.request.user.role.teacher:
            raise Http404()
        return obj

# 删除课程
class CourseDelete(DeleteView):
    model = Course
    # get = DeleteView.post
    success_url = reverse_lazy('project:course_list')
    # 只有创建该课程的教师才可以删除该课程
    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.teacher != self.request.user.role.teacher:
            raise Http404()
        return obj
# 学生加入课程
def course_select(request,pk):
    course = get_object_or_404(Course,pk=pk)
    user = get_object_or_404(User,pk=request.user.id)
    course.student.add(user.role.student)
    return HttpResponseRedirect(reverse('project:course_list_self', args=[user.id]))
# 学生退出课程
def course_cancel(request,pk):
    course = get_object_or_404(Course,pk=pk)
    user = get_object_or_404(User,pk=request.user.id)
    course.student.remove(user.role.student)
    return HttpResponseRedirect(reverse('project:course_list_self', args=[user.id]))
# 学生进入课程
# def HomeworkList(request,pk):
    # course = get_object_or_404(Course,pk=pk)
    # return render(request,'project/homework_list.html',{'course':course})
# 教师进入课程
# def HomeworkListPublished(request,pk):
#     course = get_object_or_404(Course,pk=pk)
#     return render(request,'project/homework_list_published.html',{'course':course})

#已发布作业列表
class HomeworkListPublished(ListView):
    template_name = 'project/homework_list_published.html'
    paginate_by = 5
    #教师只能查看自己发布的作业
    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.course.teacher != self.request.user.role.teacher:
            raise Http404()
        return obj
    # 按作业的发表状态来筛选获取数据集，并按发表时间逆序排列
    def get_queryset(self):
        return Homework.objects.filter(course__id=self.kwargs['pk']).filter(status='p').order_by('-published')
    # 传递额外的数据到前端
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = Course.objects.get(id=self.kwargs['pk'])
        context.update({
            'course':course,
        })
        return context

#待发布作业列表
class HomeworkListDraft(ListView):
    paginate_by = 5
    template_name = 'project/homework_list_publishing.html'
    # 用户只能看到自己的文章草稿。当用户查看别人的文章草稿时，返回http 404错误
    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.course.teacher != self.request.user.role.teacher:
            raise Http404()
        return obj
    def get_queryset(self):
        return Homework.objects.filter(course__id=self.kwargs['pk']).filter(status='d').order_by('-published')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = Course.objects.get(id=self.kwargs['pk'])
        context.update({
            'course':course,
        })
        return context

#课程作业详情
#DetailView 通过 get_object 方法来计算该作业的访问量，
# get_context_data 方法不仅传递了作业传递给模板，
# 也额外传递了该作业下的评论列表以及评论表单。
class HomeworkDetail(DetailView):
    model = Homework
    template_name = 'project/homework_detail.html'

    # 调用 homework 下的 viewed()方法来使访问量 +1
    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        obj.viewed()
        return obj

    # 覆写 get_context_data 的目的是因为除了将 homework 传递给模板外（DetailView 已经帮我们完成），
    # 还要把评论表单、homework 下的评论列表传递给模板。
    # 把评论表单、homework 下的评论列表传递给模板
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = Course.objects.get(id=self.kwargs['pkr'])
        form = CommentForm()
        comment_list = self.object.comment.filter(homework=self.object)
        context.update({
            'course':course,
            'form': form,   # 新增
            'comment_list': comment_list    # 新增
        })
        return context

#创建作业
class HomeworkCreate(CreateView):
    model = Homework
    form_class = HomeworkForm
    template_name = 'project/homework_form.html'

    # 课程字段并未在用户创建界面显示，因此需要将表单的课程字段与该课程绑定
    def form_valid(self, form):
        form.instance.course = Course.objects.get(id=self.kwargs['pk'])
        return super().form_valid(form)
#更新作业
class HomeworkUpdate(UpdateView):
    model = Homework
    form_class = HomeworkForm
    template_name = 'project/homework_form.html'

#删除作业
class HomeworkDelete(DeleteView):
    model = Homework
    get = DeleteView.post
    # 用户只能删除自己的课程
    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.course.teacher != self.request.user.role.teacher:
            raise Http404()
        return obj

    # 删除成功后跳转的地址
    def get_success_url(self):
        return reverse_lazy('project:homework_list_published',args=[str(self.kwargs['pkr'])])
    # 不需要确认模板直接删除
    # def get(self,request,*args,**kwargs):
    #     return self.post(request,*args,**kwargs)

# 将草稿发布 这里调用了 models.py 中的 publish 方法
def homework_publish(request, pk,pkr):
    homework = get_object_or_404(Homework, pk=pk)
    homework.publish()
    return redirect(reverse('project:homework_detail', args=[str(pkr),str(pk)]))

# class HandinList(ListView):
#     paginate_by = 5
#     template_name = 'project/handin_list.html'
#     def get_queryset(self):
#         return Homework.objects.get(id=self.kwargs['pk']).handin.all()

#所有作业列表
class HomeworkList(ListView):
    def get_queryset(self):
        return Homework.objects.filter(course__id=self.kwargs['pk']).filter(status='p').order_by('-published')

    # 在所有作业列表中，学生端要显示提交作业的链接，以及是否打分等信息
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = Course.objects.get(id=self.kwargs['pk'])
        homework = [x for x in self.get_queryset()]
        homework_deadline = Homework.objects.filter(course__id=self.kwargs['pk']).filter(status='p').order_by('-published').values_list('deadline')
        print(homework_deadline)
        # 定义 judge 列表为 [0,0,...]
        judge = [0 for i in range(len(homework))]
        score = []

        for each in homework:
            handin = Handin.objects.filter(homework=each,author=self.request.user.role.student)
            if len(handin):
                if handin[0].score:
                    score.append(handin[0].score)
                else:
                    score.append('未打分')

            else:
                score.append('未提交')
        # 筛选该用户提交的所有作业
        handin = Handin.objects.filter(course__id=self.kwargs['pk']).filter(author=self.request.user.role.student)
        # 若该用户已提交的作业中存在该课程相应的作业，则 judge 设为 1
        for handin in handin:
            if handin.homework in homework:
                judge[homework.index(handin.homework)] = 1

        #已超时
        homework_deadline = [homework_deadline[0] for homework_deadline in homework_deadline]
        print(homework_deadline)
        for i,homework_deadline in enumerate(homework_deadline):
            if datetime.date.today()>homework_deadline:
                # print(homework_deadline.index(homework_deadline))
                if judge[i] == 0:
                    judge[i] = 2

        # zip 函数将两个列表合并，返回一个 tuple
        info = list(zip(homework,judge,score))
        context.update({
            'course':course,
            'judge':judge,
            'info':info,
        })
        print(info)
        return context

# 已完成作业列表
class HandinListDone(ListView):
    template_name = 'project/handin_list_done.html'
    paginate_by = 5
    def get_queryset(self):
        return Handin.objects.filter(course__id=self.kwargs['pk']).filter(author=self.request.user.role.student).order_by('-id')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = Course.objects.get(id=self.kwargs['pk'])
        context.update({
            'course':course,
        })
        return context

# 创建提交的作业
class HandinCreate(CreateView):
    model = Handin
    form_class = HandinForm
    template_name = 'project/handin_form.html'

    # 课程、作业、作者字段并未在用户创建界面显示，因此需要将字段与相应信息进行绑定
    def form_valid(self, form):
        homework = Homework.objects.get(id=self.kwargs['pk'])
        course = Course.objects.get(id=self.kwargs['pkr'])
        form.instance.course = course
        form.instance.homework = homework
        form.instance.author = self.request.user.role.student
        return super().form_valid(form)

# 提交的作业详情
class HandinDetail(DetailView):
    model = Handin
    template_name = "project/handin_detail.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        homework = Homework.objects.get(id=self.kwargs['pkr'])
        context.update({
            'homework':homework,
        })
        return context

# 更新提交的作业
class HandinUpdate(UpdateView):
    model = Handin
    form_class = HandinForm
    template_name = 'project/handin_form.html'

# 删除提交的作业
class HandinDelete(DeleteView):
    model = Handin
    def get_success_url(self):
        return reverse_lazy('project:homework_list',args=[str(self.kwargs['pka'])])
    # 用户只能删除自己的作业
    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.author != self.request.user.role.student:
            raise Http404()
        return obj
    def get(self,request,*args,**kwargs):
        return self.post(request,*args,**kwargs)

# 学生作业统计
class HomeworkHandin(ListView):
    model = Handin
    template_name = 'project/homework_handin_count.html'
    # 在 Handin 提交作业表中筛选外键 homework 为该课程的作业
    def get_queryset(self):
        return Handin.objects.filter(course__id=self.kwargs['pkr']).filter(homework__id=self.kwargs['pk'])
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        homework = Homework.objects.get(id=self.kwargs['pk'])
        # 调用 models.py 中的 student_count 方法以统计学生人数
        total = Course.objects.get(id=self.kwargs['pkr']).student_count()
        # 使用 count() 方法统计属于该课程的作答作业 即已提交的作业数量
        done = Handin.objects.filter(homework=homework).count()
        context.update({
            'homework':homework,
            'total': total,
            'done': done,
        })
        return context

# 学生统计
def course_student(request,pk):
    course = Course.objects.get(pk=pk)
    student = course.student.all()
    return render(request,'project/course_student.html',context={'student':student,'course':course})

#作业评论
def homework_comment(request, pk):
    homework = get_object_or_404(Homework, pk=pk)
    comment_list = homework.comment.filter(homework=homework)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            # commit=False 的作用是仅仅利用表单的数据生成 Comment 模型类的实例，但还不保存评论数据到数据库
            comment = form.save(commit=False)
            # 将评论和被评论的文章关联起来
            comment.homework = homework
            if request.user.role.role == 1:
                comment.username = request.user.role.teacher.name
            else:
                comment.username = request.user.role.student.name
            comment.save()
            # 重定向到 homework 的详情页，实际上当 redirect 函数接收一个模型的实例时，它会调用这个模型实例的 get_absolute_url 方法
            # 然后重定向到 get_absolute_url 方法返回的 URL
            return redirect(homework)
        else:
            # 检查到数据不合法，重新渲染详情页，并且渲染表单的错误
            # 因此传三个模板变量给 detail.html：作业（Homework）、评论列表、表单 form
            context = {'homework': homework,
                       'form': form,
                       'comment_list': comment_list
                       }
            return render(request, 'homework/homework_detail.html', context=context)
    # 不是 POST 请求，说明用户没有提交数据，重定向到文章详情页
    return redirect(homework)

def score(request,pk):
    value = request.POST.get('value')
    handin = Handin.objects.get(pk=pk)
    handin.score = value
    handin.save()
    return HttpResponse("1")
import json # 新增
def get_score(request):
    course = request.GET.get('course')
    username = request.GET.get('value')
    author = User.objects.get(username=username)
    handin = Handin.objects.filter(course__id=course,author=author.role.student).order_by('homework')
    print(handin)
    homework_list = []
    score_list = []
    for each in handin:
        if each.score:
            homework_list.append(each.homework.title)
            score_list.append(each.score)
    data = {'homework':homework_list,'score':score_list}
    return HttpResponse(json.dumps(data))


#导出excel文件
def export_excel(request,pkr,pk):
    response = HttpResponse(content_type='application/vnd.ms-excel')
    homework_name =  Handin.objects.filter(course__id=pkr).filter(homework__id=pk).values('course__cname','homework__title').first()
    classes = Course.objects.filter(handin__homework__course_id=pkr).values('classes').first()
    title = classes['classes']+'——'+homework_name['course__cname']+'课程——'+homework_name['homework__title']
    # filename ='__'.join(homework_name[0])
    print(homework_name)
    response['Content-Disposition'] ='attachment;filename=homework'+datetime.datetime.now().strftime('%Y-%m-%d')+'.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('sheet1')

    alignment = xlwt.Alignment()  # Create Alignment
    alignment.horz = xlwt.Alignment.HORZ_CENTER
    ws.col(0).width = 3333
    ws.col(3).width = 3333
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    # font_style = font_style.alignment.HORZ_CENTER
    font_style.alignment = alignment
    ws.write_merge(0,0,0,4,title,font_style)

    row_num = 1
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['学号','班级','姓名','提交日期','分数']
    # columns = ['author_id','modified','score']
    username = []
    handin_obj1 = Handin.objects.filter(course__id=pkr).filter(homework__id=pk).values_list('author__user__user_id')
    for id in handin_obj1:
        author = User.objects.get(id=id[0]).username
        username.append(author)
    handin_obj = Handin.objects.filter(course__id=pkr).filter(homework__id=pk).values_list('author__classes','author__name','modified','score')

    # print(handin_obj)
    for col_num in range(len(columns)):
        ws.write(row_num,col_num,columns[col_num],font_style)

    font_style = xlwt.XFStyle()

    for row in username:
        row_num += 1
        ws.write(row_num,0,row,font_style)

    row_num = 1
    for row in handin_obj:
        row_num += 1
        for col_num in range(1,len(row)+1):
            if col_num == 3:
                font_style.num_format_str = 'M/D/YY h:mm'
                ws.write(row_num, col_num, str(row[col_num - 1]), font_style)
                font_style = xlwt.XFStyle()
            else:
                ws.write(row_num, col_num, str(row[col_num - 1]), font_style)
    wb.save(response)
    return response


#机器人接口
#username=17211010117
#学生查询自己未完成的作业
def find_homework(request):
    username=request.GET.get('username')
    try:
        author = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponse('学生用户名不存在！查询失败！ ')
    # author = User.objects.filter(username=username).get()
    # print(author)
    name =author.role.student.name
    course_id = [ id[0] for id in author.role.student.course_set.values_list('id')]
    homework_list = []
    handin_list = []
    data_list = []
    strdata =''
    for course_id in course_id:
        homework_obj =Homework.objects.filter(course_id=course_id,status='p').values_list('id')
        for id in homework_obj:
            homework_list.append(id[0])
    for homework_id in homework_list:
        handin_obj= Handin.objects.filter(author_id=author.role.student.pk,homework_id =homework_id).values_list('homework_id')
        # print(handin_obj)
        for id in handin_obj:
            handin_list.append(id[0])
    if handin_list not in handin_list:
        print(handin_list)

    handin_list = set( handin_list)  # 利用无序的概念降低复杂度
    new_list = [item for item in homework_list if item not in handin_list] #没有提交作业的id
    for homework_id in new_list:
        homework_obj= Homework.objects.filter(id=homework_id)

        for obj in homework_obj:
            data = {
                'course' : obj.course.cname,
                'title' : obj.title,
                'published' :obj.published,
                'deadline' : obj.deadline,
            }
            data_list.append(data)
    lens = len(data_list)
    strdata = name+'你目前有' + str(lens) + '项作业没有完成，请及时完成！详细情况如下:\n'
    for i,data in enumerate(data_list):
       strdata = strdata +str(i+1)+'、课程名称：'+data['course']+'\n作业标题：'+data['title']+'\n发布时间：'+data['published'].strftime('%Y-%m-%d')+'\n截止时间：'+data['deadline'].strftime('%Y-%m-%d')+'\n'
       #  strdata = strdata + '、作业标题：' + data['title'] +  '\n发布时间：' +data['published']+ '\n截止时间：'  + '\n'
    # print(data)
    return HttpResponse(strdata )
    # return HttpResponse('OK ')

#老师查询未完成作业名单
#username=hemingchao
def teacher_homework(request):
    username = request.GET.get('username')
    try:
        teacher_id = User.objects.get(username=username).role.teacher.pk
    except User.DoesNotExist:
        return HttpResponse('教师用户名不存在！查询失败！ ')
    course_obj = Course.objects.filter(teacher_id=teacher_id).values_list('id')
    course_id = [id[0] for id in course_obj]
    courseobj = Course.objects.filter(teacher_id=teacher_id)
    student_id ={}#课程id对应的学生id
    homework_id = {} #课程id对应的作业id
    teacher_name = User.objects.get(username=username).role.teacher.name

    for course in courseobj:
        student_course = []
        stu_course = course.student.values_list('id')
        for stu_course in stu_course:
           student_course.append(stu_course[0])
        student_id[course.pk]= student_course

    for course_id in course_id:
        homework_course = []
        homework_obj = Homework.objects.filter(course_id=course_id).values_list('id')
        for homework_obj in homework_obj:
            homework_course.append(homework_obj[0])
        homework_id[course_id] =homework_course
    # print(homework_id)
    # print(student_id)
    # print(len(homework_id))
    data=teacher_name+'老师您目前有'+str(len(homework_id))+'门课程，分别为：\n'
    i = 1
    for key,value in homework_id.items():
        #key:course_id value:homework_id
        course = Course.objects.get(id=key) #课程名
        # print(course)
        data = data + str(i)+ '、'+course.__str__() +' '
        i = i + 1

    data = data + '\n其中：'

    i = 1
    for key, value in homework_id.items():
        course = Course.objects.get(id=key)  # 课程名
        if len(value) > 0:
            data = data + course.__str__()+'课程有'+str(len(value))+'样作业已发布,标题分别为：\n'
        else:
            data = data + course.__str__() + '课程目前没有布置作业！\n'
        for v in value:
            # homeworkv = Homework.objects.get(id = v)
            homeworkv = Homework.objects.filter(status='p').get(id = v)
            data = data + str(i)+ '、'+ homeworkv.__str__()+' '
            i = i + 1
        if len(value) > 0:
            data = data + '\n其中:'
        # print(student_id[key])

        for v in value:
            homeworkv = Homework.objects.get(id=v)
            id= Homework.objects.get(id=v).pk
            #查找homework表中的id 没有完成作业的学生
            # print(id)
            student_not = []
            for stu_id in student_id[key]:
                handin_obj = Handin.objects.filter(homework_id=id,author_id=stu_id)
                if handin_obj.count() == 0 :
                    not_handin = Student.objects.filter(id = stu_id).values('name').get()
                    # print(not_handin)
                    student_not.append(not_handin['name'])
            student_str = '、'.join(student_not)
            data = data + '作业标题：'+homeworkv.__str__()+'  有'+ str(len(student_not))+'个没完成\n分别为:'+student_str+'\n'
        data = data + '\n'
    return HttpResponse(data)