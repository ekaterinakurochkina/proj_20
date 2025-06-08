from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название курса", help_text="Введите название курса")
    preview = models.ImageField(upload_to="materials/preview", blank=True, null=True, verbose_name="Картинка",
                                help_text="Загрузите изображение")
    description = models.TextField(blank=True, null=True, verbose_name="Описание курса",
                                   help_text="Введите описание курса")
    owner = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Владелец",
                              help_text="Укажите владельца урока")
    subscribers = models.ManyToManyField("users.User", null=True, blank=True, verbose_name="Подписчики", help_text="Укажите подписчиков", related_name="subscribers")

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название курса", help_text="Введите название курса")
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, verbose_name="Курс", help_text="Выберите курс",
                               blank=True, null=True, related_name='lessons')
    description = models.TextField(blank=True, null=True, verbose_name="Описание курса",
                                   help_text="Введите описание курса")
    preview = models.ImageField(upload_to="materials/preview", blank=True, null=True, verbose_name="Картинка",
                                help_text="Загрузите изображение")
    video_url = models.URLField(max_length=200, verbose_name="Ссылка на видео")
    owner = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Владелец",
                              help_text="Укажите владельца курса")

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class Subscription(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, null=True, blank=True, verbose_name="Пользователь",
                             help_text="Укажите пользователя", related_name='subscriber')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс",
                               help_text="Выберите курс для подписки на обновления",
                               blank=True, null=True, related_name='subscription')
    is_subscription = models.BooleanField(default=False, verbose_name="Подписка на обновления",
                                          help_text="Подпишитесь на обновления")

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"