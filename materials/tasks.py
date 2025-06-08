from config.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from celery import  shared_task
from .models import Course, Lesson


@shared_task
def send_course_update_email(email_list):
    message = "Курс, на который Вы подписаны, был обновлён."
    send_mail(
        "Обновление курса", message, EMAIL_HOST_USER, email_list
    )

