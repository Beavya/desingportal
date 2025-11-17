from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Application(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название заявки")
    description = models.TextField(verbose_name="Описание")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    admin_comment = models.TextField(blank=True, verbose_name="Комментарий администратора")

    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_progress', 'Принято в работу'),
        ('completed', 'Выполнено'),
    ]

    image = models.ImageField(
        upload_to='applications/',
        verbose_name="Фото помещения или план",
    )

    design_image = models.ImageField(
        upload_to='designs/',
        verbose_name="Готовый дизайн",
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name="Статус заявки"
    )

    def __str__(self):
        return f"{self.title} ({self.user.username})"

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-created_at']