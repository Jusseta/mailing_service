from django.db import models

from mailing.models import NULLABLE


class Blog(models.Model):
    """Модель блога"""
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержимое статьи')
    image = models.ImageField(upload_to='blog/', verbose_name='Изображение', **NULLABLE)
    views = models.PositiveIntegerField(default=0, verbose_name='Количество просмотров')
    published_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'
