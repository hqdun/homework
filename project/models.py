from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from datetime import datetime   # 新增
import uuid                     # 新增
import os                       # 新增
# 自定义文件上传路径
def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    sub_folder = 'file'
    if ext.lower() in ["jpg", "png", "gif"]:
        sub_folder = "images"
    if ext.lower() in ["pdf", "docx","xlsx","rar","zip","7z"]:
        sub_folder = "document"
    # if ext.lower() in ["rar","zip","7z"]:
    #     sub_folder = "winrar"
    # 路径与教师的 id 绑定
    return os.path.join(str(instance.course.teacher.id), sub_folder, filename)


class Role(models.Model):
    ROLE_CHOICES = (
        (0,'学生'),
        (1,'教师')
    )
    user = models.OneToOneField(User,related_name='role',on_delete=models.CASCADE)
    role = models.SmallIntegerField(choices=ROLE_CHOICES,default=0,verbose_name='角色')
 
    def __str__(self):
    	return str(self.role)
 
'''
    定义一个抽象类，字段为各个表的公共字段，这个类并不会在数据库中建表
'''
class UserAbstractModel(models.Model):
    GENDER_CHOICES = (
        (0,'男'),
        (1,'女')
    )
    name = models.CharField('姓名',default='', max_length=50)
    gender = models.SmallIntegerField(choices=GENDER_CHOICES,default=0,verbose_name='性别')
    created = models.DateTimeField('创建时间', auto_now_add=True)
    modified = models.DateTimeField('最后更改时间', auto_now=True)
    description = models.TextField('个人描述',null=True)
    # photo = models.ImageField('用户头像',upload_to=user_directory_path,blank=True)
 
    class Meta:
        abstract = True
 
class Teacher(UserAbstractModel):
    user = models.OneToOneField(Role,related_name='teacher',on_delete=models.CASCADE)#一对一
    ranks = models.CharField(default='无', max_length=50,verbose_name='职称')
 
    def __str__(self):
        return self.name
 
    class Meta:
        verbose_name='教师表'
        verbose_name_plural = verbose_name
 
class Student(UserAbstractModel):
    user = models.OneToOneField(Role,related_name='student',on_delete=models.CASCADE)#一对一
    classes = models.CharField('班级',default='', max_length=50)
 
    def __str__(self):
        return self.user.user.username
 
    def get_course_count(self):
    	return Course.objects.filter(student__id=self.id).count()
 
    class Meta:
        verbose_name='学生表'
        verbose_name_plural = verbose_name

'''课程的模型类'''
class Course(models.Model):
    cname = models.CharField(verbose_name='课程名称', max_length=50,null=False)
    classes =  models.CharField(verbose_name='班级',default='', max_length=50)
    description = models.TextField(verbose_name='课程描述',)
    tag = models.CharField(verbose_name='标签', max_length=50,default='django')
    teacher = models.ForeignKey(Teacher,related_name="course",on_delete=models.CASCADE)#teacher_id
    student = models.ManyToManyField(Student,blank=True)#多对多
    def __str__(self):
        return self.cname
    def get_absolute_url(self):
        return reverse('project:course_detail', args=[str(self.pk)])
    def student_count(self):
        return self.student.count()
    class Meta:
        verbose_name='课程'
        verbose_name_plural = verbose_name

#发布作业与提交作业的抽象类
class WorkAbstractModel(models.Model):
    # body = models.TextField('正文')
    body = RichTextUploadingField('正文')
    created = models.DateTimeField('创建时间', auto_now_add=True)
    modified = models.DateTimeField('修改时间', auto_now=True)
    file = models.FileField('文件',upload_to=user_directory_path,blank=True)
    class Meta:
        abstract = True # 抽象类

#发布作业的模型类
class Homework(WorkAbstractModel):
    STATUS_CHOICES = (
        ('d', '草稿'),
        ('p', '发表'),
    )
    title = models.CharField('标题', max_length=200)
    published = models.DateTimeField('发布时间', null=True)
    status = models.CharField('作业状态', max_length=1, choices=STATUS_CHOICES, default='p')
    views = models.PositiveIntegerField('浏览量', default=0)
    deadline = models.DateField('截止时间', null=True)
    course = models.ForeignKey(Course,related_name="homework",on_delete=models.CASCADE)#couse_id
    def __str__(self):
        return self.title
    # 快速获取文件格式
    def get_format(self):
        return self.file.url.split('.')[-1].upper()
    # Django 的 CreateView 和 UpdateView 在完成对象的创建或编辑后会自动跳转到这个绝对 url
    def get_absolute_url(self):
        return reverse('project:homework_detail', args=[str(self.course.id),str(self.pk)])
    def clean(self):
        if self.status == 'd' and self.published is not None:
            self.published = None
            # raise ValidationError('草稿没有发布日期. 发布日期已清空。')
        if self.status == 'p' and self.published is None:
            self.published = datetime.now()
    # 浏览量 +1
    def viewed(self):
        self.views += 1
        self.save(update_fields=['views'])
    # 发布编辑好的草稿，增加发布时间
    def publish(self):
        self.status = 'p'
        self.published = datetime.now()
        self.save(update_fields=['status', 'published'])
    class Meta:
        ordering = ['-modified']
        verbose_name = "作业"
        verbose_name_plural = verbose_name

#提交作业的模型类
class Handin(WorkAbstractModel):
    author = models.ForeignKey(Student,related_name="handin",on_delete=models.CASCADE) #models.CASCADE级联删除 to_field不写自动关联id  #author_id
    course = models.ForeignKey(Course,related_name="handin",on_delete=models.CASCADE)  #couser_id
    homework =  models.ForeignKey(Homework,related_name="handin",on_delete=models.CASCADE) #homework_id
    score = models.IntegerField('分数',null=True)
    def __str__(self):
        return self.author.name
    #快速获取文件格式
    def get_format(self):
        return self.file.url.split('.')[-1].upper()
    # Django 的 CreateView 和 UpdateView 在完成对象的创建或编辑后会自动跳转到这个绝对 url
    def get_absolute_url(self):
        return reverse('project:handin_detail', args=[str(self.homework.course.id),str(self.homework.pk),str(self.pk)])
    class Meta:
        verbose_name = "作答"
        verbose_name_plural = verbose_name

#作业评论的模型类
class Comment(models.Model):
    homework = models.ForeignKey(Homework,related_name="comment",on_delete=models.CASCADE)
    text = models.TextField('评论内容')
    created = models.DateTimeField('评论时间',auto_now_add=True)
    username = models.CharField('用户名称',max_length=50)
    def __str__(self):
        return self.text[:20]
    class Meta:
        verbose_name = "评论"
        verbose_name_plural = verbose_name