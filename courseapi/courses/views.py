from django.shortcuts import render

# Create your views here.


# from django.http import HttpResponse
#
# def index(request):
#     return HttpResponse("Hello, World!")

from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response

from courses.models import Category, Course, Lesson
from courses import serializers, paginators


# không được viewsets.ModelViewSet vì nó sẽ hiện thực hóa tất cả api
# ViewSet chỉ hiện thực hóa layout co bản, generics.ListAPi hiện thực hóa api lấy danh sách (chỉ hiện thực hóa một cái này thôi)
class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.filter(active=True)
    serializer_class = serializers.CategorySerializer


class CourseViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Course.objects.filter(active=True)
    serializer_class = serializers.CourseSerializer
    pagination_class = paginators.CoursePagination


    def get_queryset(self):
        queryset = self.queryset

        q = self.request.query_params.get('q')
        if q:
            queryset = queryset.filter(subject__icontains=q)

        cate_id = self.request.query_params.get('cate_id')
        if cate_id:
            queryset = queryset.filter(category_id=cate_id)

        return queryset


    @action(methods=['get'], detail=True, url_path='lessons')
    def get_lessons(self, request, pk):
        lessons = self.get_object().lesson_set.filter(active=True)

        return Response(serializers.LessonSerializer(lessons, many=True).data,status = status.HTTP_200_OK)



class LessonViewSet(viewsets.ViewSet,generics.RetrieveAPIView):
    queryset = Lesson.objects.filter(active=True)
    serializer_class = serializers.LessonDetailsSerializer

