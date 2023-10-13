from django.conf import settings
from django.db import models
from django.utils import timezone


NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    """Модель клиента"""
    full_name = models.CharField(max_length=150, verbose_name='ФИО')
    email = models.EmailField(max_length=150, verbose_name='Почта')
    message = models.TextField(verbose_name='Комментарий', **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='Владелец', **NULLABLE)

    def __str__(self):
        return f'{self.full_name} ({self.email})'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'


class Message(models.Model):
    """Сообщение для рассылки"""
    theme = models.CharField(max_length=100, verbose_name='Тема сообщения')
    body = models.TextField(verbose_name='Текст')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='Владелец', **NULLABLE)

    def __str__(self):
        return self.theme

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'


class Mailing(models.Model):
    """Модель рассылки"""
    frequency_list = [
        ('day', 'раз в день'),
        ('week', 'раз в неделю'),
        ('month', 'раз в месяц')
    ]

    status_list = [
        ('finish', 'завершена'),
        ('create', 'создана'),
        ('start', 'запущена')
    ]

    start_time = models.DateTimeField(default=timezone.now, verbose_name='Дата начала рассылки')
    stop_time = models.DateTimeField(verbose_name='Дата окончания рассылки', **NULLABLE)

    frequency = models.CharField(choices=frequency_list, default='day', verbose_name='Периодичность')
    status = models.CharField(choices=status_list, default='create', verbose_name='Статус')
    is_active = models.BooleanField(default=True, verbose_name='Активна')

    mail_to = models.ManyToManyField(Client, verbose_name='Получатель')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='Сообщение', **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='Владелец', **NULLABLE)

    def __str__(self):
        return self.status

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'


class MailingLogs(models.Model):
    """Модель логов рассылки"""
    status_list = [
        ('success', 'успешно'),
        ('failure', 'неудачно')
    ]

    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='Рассылка')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Клиент')

    last_try = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время отправки')
    status = models.CharField(choices=status_list, default='success', verbose_name='Статус попытки')
    server_response = models.TextField(verbose_name='Ответ почтового сервера', **NULLABLE)

    def __str__(self):
        return f'Последняя попытка была {self.last_try}, статус "{self.status}"'

    class Meta:
        verbose_name = 'лог'
        verbose_name_plural = 'логи'
