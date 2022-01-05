from django.contrib import admin
from .models import *
from django.utils.html import format_html
admin.site.site_header = '作业管理系统'
admin_order_field = ('modified',) # 指定方法排序
class StudentAdmin(admin.ModelAdmin):
    '''设置列表可显示的字段'''
    list_display = ('name','gender','created','modified',)
    '''设置过滤选项'''
    # list_filter = ('',)
    '''每页显示条目数'''
    list_per_page = 5
    '''设置可编辑字段'''
    list_editable = ()
    '''按日期月份筛选'''
    date_hierarchy = 'created'
    '''按发布日期排序'''
    ordering = ('-created',)
    '''下拉菜单修改'''
    # raw_id_fields = ('',)
    # readonly_fields = ('',)
    '''设置带链接字段'''
    # list_display_links = ('',)
    '''可搜索字段'''
    search_fields = ('name',)
    '''多对多字段'''
    # filter_horizontal = ('',)
admin.site.register(Student, StudentAdmin)
class CourseInline(admin.TabularInline):
    model = Course
    fields = ('cname', 'classes', 'opened',)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name','gender','created','modified',)
    list_per_page = 5
    list_editable = ()
    date_hierarchy = 'created'
    ordering = ('-created',)
    # inlines = [
    #     CourseInline,
    # ]
    search_fields = ('name',)
admin.site.register(Teacher, TeacherAdmin)
class HomeworkInline(admin.TabularInline):
    model = Homework
    fields = ('title', 'status')
class CourseAdmin(admin.ModelAdmin):
    list_display = ('cname','classes')
    list_per_page = 5
    inlines = [
        HomeworkInline,
    ]
    raw_id_fields = ('teacher',)
    search_fields = ('cname',)
admin.site.register(Course, CourseAdmin)
class HandinInline(admin.TabularInline):
    model = Handin
    fields = ('course','author','score',)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ('title','status','created','modified','handin_count')
    list_filter = ('status','published',)
    list_per_page = 5
    list_editable = ('status',)
    inlines = [
        HandinInline,
    ]
    raw_id_fields = ('course',)
    list_display_links = ('title',)
    date_hierarchy = 'modified'
    ordering = ('-modified',)
    search_fields = ('title',)
    def handin_count(self,obj):
        count = len(obj.handin.all())
        if count:
            return count
        else:
            return format_html(
                    '<span style="color:red;">暂无人提交</span>',
                )
    handin_count.short_description = '已提交作业数量'
    '''自定义actions'''
    actions = ['make_published']
    def make_published(self, request, queryset):
        queryset.update(status='p')
    make_published.short_description = "发布所选作业"
admin.site.register(Homework, HomeworkAdmin)
class HandinAdmin(admin.ModelAdmin):
    list_display = ('course','homework',)
    list_filter = ('course','created',)
    list_per_page = 5
    list_display_links = ('homework',)
    raw_id_fields = ('course','homework','author',)
    search_fields = ('homework',)
admin.site.register(Handin, HandinAdmin)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('homework','username','created','text',)
    list_filter = ('homework',)
    list_per_page = 5
    list_display_links = ('homework',)
    raw_id_fields = ('homework',)
    search_fields = ('homework',)
admin.site.register(Comment, CommentAdmin)
