from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')
    avatar = models.ImageField(upload_to='users/avatars/', verbose_name='Аватар', blank=True, null=True)
    phone_number = models.CharField(max_length=15, verbose_name='Телефон', blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    token = models.CharField(max_length=100, verbose_name='Токен', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ["email",]
        permissions = [
            ("can_view_user", "Can view User"),
        ]


    def __str__(self):
        return self.email
