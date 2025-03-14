from courses.models import Category, Course, Lesson, Tag
from rest_framework import serializers

# from cloudinary.http_client import HttpClient


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name']


class ItemSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)

        data['image'] = instance.image.url

        return data


class CourseSerializer(ItemSerializer):
    class Meta:
        model = Course
        fields = ['id','subject','image','created_date','cate_id']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class LessonSerializer(ItemSerializer):
    class Meta:
        model = Lesson
        fields = ['id' ,'subject','image','courses_id','created_date','updated_date']


class LessonDetailsSerializer(LessonSerializer):
    tags = TagSerializer(many= True)

    class Meta:
        model = LessonSerializer.Meta.model
        fields = LessonSerializer.Meta.fields + ['tags'] #+ ['content','tags']
#
# class CourseSerializer(serializers.ModelSerializer):
#     image = serializers.SerializerMethodField()
#     class Meta:
#         model = Course
#         fields = ['id','subject','image','created_date','category_id']
#
#     def get_image(self, obj):
#         return obj.image.url