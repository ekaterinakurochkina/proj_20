from django.db.models import CASCADE
from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name="Email", help_text="Укажите почту")

    phone = models.CharField(max_length=35, verbose_name="Телефон", blank=True, null=True,
                             help_text="Введите номер телефона")
    avatar = models.ImageField(upload_to="users/avatars", verbose_name="Аватар", blank=True, null=True,
                               help_text='Загрузите свой аватар')

    city = models.CharField(max_length=50, verbose_name="Город", blank=True, null=True,
                            help_text="Введите название города")



    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['email']



class Payments(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="Пользователь", help_text="Пользователь",
                             blank=True, null=True, related_name='payments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True, related_name="payments", verbose_name="Оплаченный курс")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True, related_name="payments", verbose_name="Оплаченный урок")

    payment_date = models.DateTimeField(verbose_name="Дата оплаты", auto_now_add=True, help_text="Введите дату оплаты",
                                        null=False, blank=True)

    payment_amount = models.PositiveIntegerField(verbose_name="Сумма оплаты", help_text="Сумма оплаты", null=False,
                                                 blank=False)
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Наличные'),
        ('transfer', 'Перевод'),
    ]

    payment_method = models.CharField(
        max_length=15,
        choices=PAYMENT_METHOD_CHOICES,
        verbose_name="Метод оплаты",
        help_text="Выберите метод оплаты: наличные или перевод.",
        default='transfer'
    )

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
        ordering = ['user']