from django.core.serializers import serialize
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView, \
    get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from .paginators import MaterialsPaginator
from .tasks import send_course_update_email
from rest_framework.response import Response
from rest_framework.decorators import action


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = MaterialsPaginator

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def update(self, request, *args, **kwargs):
        course = self.get_object()

        # Получаем список подписчиков курса
        mail_list = list(course.subscribers.values_list('email', flat=True))

        # Обновляем курс
        serializer = self.get_serializer(course, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Если обновление прошло успешно, отправляем уведомления подписчикам
        if mail_list:
            send_course_update_email.delay(mail_list)

        return Response(serializer.data, status=status.HTTP_200_OK)


class LessonCreateApiView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListApiView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    # permission_classes = (IsAuthenticated)
    pagination_class = MaterialsPaginator

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.query_params.get('pk'):
            queryset = queryset.filter(course_id=int(self.request.query_params.get('pk')))
        return queryset


class LessonRetrieveApiView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    # permission_classes = (IsAuthenticated, IsModer | IsOwner)


class LessonUpdateApiView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    # permission_classes = (IsAuthenticated, IsModer | IsOwner)


class LessonDestroyApiView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    # permission_classes = (IsAuthenticated, ~IsModer, IsOwner)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Subscription, Course


class SubscriptionApiView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get("id")
        course_item = get_object_or_404(Course, id=course_id)

        subs_item = Subscription.objects.filter(user=user, course=course_item)

        # Если подписка у пользователя на этот курс есть - удаляем ее
        if subs_item.exists():
            subs_item.delete()
            message = "подписка удалена"
            status_code = status.HTTP_200_OK
        # Если подписки у пользователя на этот курс нет - создаем ее
        else:
            subs_item.create()
            message = "подписка добавлена"
            status_code = status.HTTP_201_CREATED

        # Возвращаем ответ в API
        return Response({"message": message}, status=status_code)
