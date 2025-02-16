from django.db import models


class Recipient(models.Model):
    email = models.CharField(
        unique=True,
        max_length=150, verbose_name="Email клиента", help_text="Введите email клиента"
    )
    name = models.CharField(
        max_length=150,
        verbose_name="Ф.И.О. клиента",
        help_text="Введите Ф.И.О. клиента",
    )
    comment = models.TextField(
        blank=True,
        null=True,
        verbose_name="Комментарий",
        help_text="Введите комментарий",
    )

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        ordering = [
            "name",
        ]

    def __str__(self):
        return self.name


class Message(models.Model):
    subject = models.CharField(
        max_length=150, verbose_name="Тема письма", help_text="Введите тему письма"
    )
    letter_body = models.TextField(
        blank=True,
        null=True,
        verbose_name="Текст письма",
        help_text="Введите содержимое письма",
    )

    class Meta:
        verbose_name = "Письмо"
        verbose_name_plural = "Письма"

    def __str__(self):
        return self.subject


class Newsletter(models.Model):
    '''Модель «Рассылка»'''
    COMPLETED = 'completed'
    CREATED = 'created'
    LAUNCHED = 'launched'

    STATUS = [
        (COMPLETED, 'Завершена'),
        (CREATED, 'Создана'),
        (LAUNCHED, 'Запущена'),
    ]
    # Дата и время первой отправки (datetime)
    date_and_time_of_first_dispatch = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Первая отправка",
        help_text="Дата и время первой отправки",
    )
    # Дата и время окончания отправки (datetime)
    date_and_time_of_end_of_sending = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Окончание отправки",
        help_text="Дата и время окончания отправки ",
    )
    # Статус (строка: 'Завершена', 'Создана', 'Запущена').
    status = models.CharField(
        max_length=9,
        choices=STATUS,
        verbose_name='Статус рассылки'
    )
    # Сообщение (внешний ключ на модель «Сообщение»).
    message = models.ForeignKey(
        Message,
        verbose_name="Сообщение",
        help_text="Укажите сообщение рассылки",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="newsletters",
    )
    # Получатели («многие ко многим», связь с моделью «Получатель»).
    recipients = models.ManyToManyField(
        Recipient,
        verbose_name="Получатели",
        help_text="Укажите получателей рассылки",
    )

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"

    def __str__(self):
        return f'{self.date_and_time_of_first_dispatch} {self.status}'