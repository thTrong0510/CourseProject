from django.contrib import admin
from courses.models import Category, Course, Lesson
from django.utils.html import mark_safe
from django import forms
from ckeditor_uploader.widgets import  CKEditorUploadingWidget
from django.urls import path
from django.template.response import TemplateResponse
from django.db.models import Count

class LessonForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)
    class Meta:
        model = Lesson
        fields = '__all__'

class MyCourseAdmin(admin.ModelAdmin):
    readonly_fields = ['image_view']
    def image_view(self, course):
        return mark_safe(f"<img src='/static/{course.image}' width='120' />")

class MyLessonAdmin(admin.ModelAdmin):
    form = LessonForm

#comment edit lai page admin
# admin.site.register(Category)
# admin.site.register(Course, MyCourseAdmin)
# admin.site.register(Lesson, MyLessonAdmin)

#edit lai giao dien trang admin
class CourseAppAdminSite(admin.AdminSite):
    site_header = 'Hệ thống khoá học trực tuyến'

    def get_urls(self):
        return [
            path('course-stats/', self.stats_view)
        ] + super().get_urls()

    def stats_view(self, request):
        count = Course.objects.filter(active=True).count()
        stats = Course.objects.annotate(lesson_count=Count('my_lesson')).values('id', 'subject', 'lesson_count')
        return TemplateResponse(request,'admin/course-stats.html', {'course_count': count,'course_stats': stats})

admin_site = CourseAppAdminSite(name='myadmin')

admin_site.register(Category)
admin_site.register(Course, MyCourseAdmin)
admin_site.register(Lesson, MyLessonAdmin)

# Register your models here.
