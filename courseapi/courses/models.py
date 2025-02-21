from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField
# Create your models here.

#ke thua User mac dinh
class User(AbstractUser):
    pass

class BaseModel(models.Model):
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    #meta ko duoc ke thua
    class meta:
        abstract = True

class Category(BaseModel):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Course(BaseModel):
    subject = models.CharField(max_length=255)
    description = models.TextField(null=True)
    image = models.ImageField(upload_to='courses/%y/%m')#duong dan tuyet doi da cau hinh o setting

    cate = models.ForeignKey(Category, on_delete=models.PROTECT)

    def __str__(self):
        return self.subject
    class Meta:
        ordering = ['-id']

class Lesson(BaseModel):
    subject = models.CharField(max_length=255)
    content = RichTextField
    image = models.ImageField(upload_to='lesson/%Y/%M')
    courses = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.subject