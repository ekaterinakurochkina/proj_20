from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User  # Предполагается, что у вас есть модель User
from .models import Lesson, Course, Subscription


class MaterialsTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test@test.ru")
        self.course = Course.objects.create(
            name="test_course", description="test_description", owner=self.user
        )
        self.lesson = Lesson.objects.create(
            name="test_lesson", course=self.course, owner=self.user
        )
        self.ubscription = Subscription.objects.create(course=self.course, user=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        """Тестирование просмотра урока"""
        url = reverse("materials:lessons_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.lesson.name)

    def test_lesson_create(self):
        """Тестирование создания урока"""
        url = reverse("materials:lessons_create")
        data = {
            "name": "Геометрические фигуры",
            "description": "Простейшие фигуры",
            "preview": None,
            "video_url": "https://www.youtube.com/testlesson/",
            "course": 1,
            "payment": {}
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        """Тестирование обновления урока"""
        url = reverse("materials:lessons_update", args=(self.lesson.pk,))
        data = {"name": "Урок_New"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "Урок_New")

    def test_lesson_delete(self):
        """Тестирование удаления урока"""
        url = reverse("materials:lessons_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        """Тестирование просмотра списка уроков"""
        url = reverse("materials:lessons_list")
        response = self.client.get(url)
        data = response.json()
        print(data)
        result = data["results"]
        print(result)
        res = len(result[0])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(res, 6)

    def test_subscription(self):
        url = reverse("materials:subscription", args=(self.course.pk,))
        data = {"id": 1, "is_subscription": True, "user": self.user.pk, "course": self.course.pk,
                "course_id": self.course.pk}
        print(data)

        response = self.client.post(url, data)
        print(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("message"), "подписка удалена")