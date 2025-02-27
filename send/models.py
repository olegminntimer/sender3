from django.db import models

from users.models import CustomUser


class Recipient(models.Model):
    email = models.CharField(
        unique=True, max_length=150, verbose_name="Email получателя", help_text="Введите email получателя"
    )
    name = models.CharField(
        max_length=150,
        verbose_name="Ф.И.О. получателя",
        help_text="Введите Ф.И.О. получателя",
    )
    comment = models.TextField(
        blank=True,
        null=True,
        verbose_name="Комментарий",
        help_text="Введите комментарий",
    )
    owner = models.ForeignKey(
        CustomUser,
        verbose_name="Владелец списка получателей",
        help_text="Укажите владельца списка получателей",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )  # Владелец списка получателей.

    class Meta:
        verbose_name = "получатель"
        verbose_name_plural = "получатели"
        ordering = [
            "email",
        ]
        permissions = [
            ("can_view_recipient", "Can view Recipient"),
        ]

    def __str__(self):
        return self.name


class Message(models.Model):
    subject = models.CharField(max_length=150, verbose_name="Тема письма", help_text="Введите тему письма")
    letter_body = models.TextField(
        blank=True,
        null=True,
        verbose_name="Текст письма",
        help_text="Введите содержимое письма",
    )
    owner = models.ForeignKey(
        CustomUser,
        verbose_name="Владелец сообщения",
        help_text="Укажите владельца сообщения",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )  # Владелец сообщения.

    class Meta:
        verbose_name = "письмо"
        verbose_name_plural = "письма"
        ordering = [
            "subject",
        ]
        permissions = [
            ("can_view_message", "Can view Message"),
        ]

    def __str__(self):
        return self.subject


class Newsletter(models.Model):
    """Модель «Рассылка»"""

    COMPLETED = "completed"
    CREATED = "created"
    LAUNCHED = "launched"

    STATUS = [
        (COMPLETED, "Завершена"),
        (CREATED, "Создана"),
        (LAUNCHED, "Запущена"),
    ]
    # Дата и время первой отправки (datetime)
    first_dispatch = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Первая отправка",
        help_text="Дата и время первой отправки",
    )
    # Дата и время окончания отправки (datetime)
    end_of_sending = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Окончание отправки",
        help_text="Дата и время окончания отправки ",
    )
    # Статус (строка: 'Завершена', 'Создана', 'Запущена').
    status = models.CharField(max_length=9, choices=STATUS, default=CREATED, verbose_name="Статус рассылки", blank=True, null=True,)
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
    owner = models.ForeignKey(
        CustomUser,
        verbose_name="Владелец рассылки",
        help_text="Укажите владельца рассылки",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )  # Владелец рассылки.

    class Meta:
        verbose_name = "рассылка"
        verbose_name_plural = "рассылки"
        ordering = [
            "id",
        ]
        permissions = [
            ("can_view_newsletter", "Can view Newsletter"),
        ]

    def __str__(self):
        return f"{self.first_dispatch} {self.status}"


class AttemptToSend(models.Model):
    """Модель «Попытка рассылки»"""

    SUCCESSFULLY = "successfully"
    NOT_SUCCESSFULLY = "not_successfully"

    STATUS = [
        (SUCCESSFULLY, "Успешно"),
        (NOT_SUCCESSFULLY, "Не успешно"),
    ]
    # Дата и время попытки (datetime).
    attempt = models.DateTimeField(
        auto_now=True,
        blank=True,
        null=True,
        verbose_name="Дата и время попытки",
        help_text="Дата и время попытки рассылки",
    )
    # Статус (строка: 'Успешно', 'Не успешно').
    status = models.CharField(max_length=16, choices=STATUS, blank=True, null=True, verbose_name="Статус попытки рассылки")
    # Ответ почтового сервера (текст).
    mail_server_response = models.CharField(
        max_length=200, blank=True, null=True, verbose_name="Ответ почтового сервера"
    )
    # Рассылка (внешний ключ на модель «Рассылка»).
    newsletter = models.ForeignKey(
        Newsletter,
        verbose_name="Рассылка",
        help_text="Укажите рассылку",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="attempt_to_send_list",
    )
    # owner = models.ForeignKey(
    #     CustomUser,
    #     verbose_name="Владелец попытки рассылки",
    #     help_text="Укажите владельца попытки рассылки",
    #     blank=True,
    #     null=True,
    #     on_delete=models.SET_NULL,
    # )  # Владелец попытки рассылки.

    class Meta:
        verbose_name = "попытка рассылки"
        verbose_name_plural = "попытки рассылки"
        ordering = [
            "attempt",
        ]

    def __str__(self):
        return f"{self.attempt} {self.status}"
