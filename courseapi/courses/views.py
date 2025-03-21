from rest_framework.decorators import action
from rest_framework.response import Response

from courses.models import Category, Course, Lesson, User, Comment, Like
from courses import serializers, paginators, perms
from rest_framework import viewsets, generics, parsers, permissions, status


class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.filter(active=True)
    serializer_class = serializers.CategorySerializer


class CourseViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Course.objects.filter(active=True)
    serializer_class = serializers.CourseSerializer
    # pagination_class = paginators.CoursePaginator

    def get_queryset(self):
        query = self.queryset

        q = self.request.query_params.get('q')
        if q:
            query = query.filter(subject__icontains=q)

        cate_id = self.request.query_params.get('category_id')
        if cate_id:
            query = query.filter(category_id=cate_id)

        return query


    @action(methods=['get'], url_path='lessons', detail=True)
    def get_lessons(self, request, pk):
        lessons = self.get_object().lesson_set.filter(active=True)
        return Response(serializers.LessonSerializer(lessons, many=True).data)


class LessonViewSet(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = Lesson.objects.prefetch_related('tags').filter(active=True)
    serializer_class = serializers.LessonDetailsSerializer

    def get_permissions(self):
        if self.action.__eq__('get_comments'):
            if self.request.method.__eq__('POST'):
                return [permissions.IsAuthenticated()]
        elif self.action.__eq__('like'):
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=['get', 'post'], url_path='comments', detail=True)
    def get_comments(self, request, pk):
        if request.method.__eq__('POST'):
            t = serializers.CommentSerializer(data={
                'content': request.data.get('content'),
                'user': request.user.pk,
                'lesson': pk
            })
            t.is_valid(raise_exception=True)
            c = t.save()
            return Response(serializers.CommentSerializer(c).data, status=status.HTTP_201_CREATED)
        else:
            comments = self.get_object().comment_set.select_related('user').filter(active=True)
            p = paginators.CommentPaginator()
            page = p.paginate_queryset(comments, self.request)
            if page is not None:
                serializer = serializers.CommentSerializer(page, many=True)
                return p.get_paginated_response(serializer.data)
            else:
                return Response(serializers.CommentSerializer(comments, many=True).data)


    @action(methods=['post'], url_path='like', detail=True)
    def like(self, request, pk):
        li, created = Like.objects.get_or_create(user=request.user, lesson=self.get_object())
        if not created:
            li.active = not li.active
        li.save()
        return Response(serializers.LessonDetailsSerializer(self.get_object(), context={'request': self.request}).data)


class CommentViewSet(viewsets.ViewSet, generics.DestroyAPIView, generics.UpdateAPIView, generics.ListAPIView):
    queryset = Comment.objects.filter(active=True)
    serializer_class = serializers.CommentSerializer
    permission_classes = [perms.CommentOwner]

    # def delete(self, request, item_id):
    #     try:
    #         # Retrieve Iten by ID
    #         item = Comment.objects.get(id=item_id)
    #
    #     except Comment.DoesNotExist:
    #         return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
    #
    #     # Delete the item from the database
    #     item.delete()
    #
    #     # Return a 284 response
    #     return Response(status=status.HTTP_284_NO_CONTENT)


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView, generics.UpdateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = serializers.UserSerializer
    parser_classes = [parsers.MultiPartParser]

    @action(methods=['get', 'patch'], url_path='current-user', detail=False, permission_classes=[permissions.IsAuthenticated])
    def get_current_user(self, request):
        if request.method__eq__("PATCH"):
            u = request.user
            for key in request.data:
                if key in ['first_name', 'last_name', 'avatar']:
                    setattr(u, key, request.data[key])
            u.save()
            return Response(serializers.UserSerializer(u).data)
        return Response(serializers.UserSerializer(request.user).data)