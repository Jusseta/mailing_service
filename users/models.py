from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from mailing.models import NULLABLE


class User(AbstractUser):
    """Класс пользователя"""
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')

    is_active = models.BooleanField(default=False, verbose_name='активность')
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    phone = models.CharField(max_length=35, verbose_name='номер телефона', **NULLABLE)
    country = models.CharField(max_length=50, verbose_name='страна', **NULLABLE)

    token = models.CharField(max_length=250, verbose_name='токен', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
