from celery import shared_task
from config.settings import EMAIL_HOST_USER
from django.core.mail import send_mail


@shared_task
def send_course_update_email(email_list):
    """Функция отправляет подписчикам сообщения об обновлении курса"""
    message = "Курс, на который Вы подписаны, был обновлён."
    send_mail(
        "Обновление курса", message, EMAIL_HOST_USER, email_list
    )


@shared_task
def check_users_is_active():
    """Функция проверяет, что пользователь не заходил больше месяца и блокирует его"""
    today = timezone.now()
    last_month = today - timedelta(days=32)
    users = User.objects.all()

    for user in users:
        if user.last_login is not None and user.last_login < last_month:
            user.is_active = False
            user.save()
