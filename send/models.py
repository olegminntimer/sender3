from django.db import models

# Create your models here.
class Newsletter(models.Model):
    '''Модель рассылки'''
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