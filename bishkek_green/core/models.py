from django.db import models
from django.contrib.auth.models import User


class TreeType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='tree_types/', blank=True, null=True)

    def __str__(self):
        return self.name


class GreenLocation(models.Model):
    STATUS_CHOICES = [
        ('planned', 'Запланировано'),
        ('in_progress', 'В процессе'),
        ('completed', 'Завершено'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Информация о локации
    area_size = models.PositiveIntegerField(help_text="Размер территории в кв.м", blank=True, null=True)
    trees_planted = models.PositiveIntegerField(default=0)

    # Дополнительные характеристики
    image = models.ImageField(upload_to='locations/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class PlantingRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'На рассмотрении'),
        ('approved', 'Одобрено'),
        ('rejected', 'Отклонено'),
        ('completed', 'Выполнено'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Связь с пользователем
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    description = models.TextField()
    preferred_tree_type = models.ForeignKey(TreeType, on_delete=models.SET_NULL, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    admin_notes = models.TextField(blank=True)

    def __str__(self):
        return f"Заявка от {self.name}: {self.address}"


class Donation(models.Model):
    DONATION_TYPES = [
        ('money', 'Денежная помощь'),
        ('trees', 'Саженцы'),
        ('materials', 'Материалы'),
        ('volunteer', 'Волонтёрство'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    donation_type = models.CharField(max_length=20, choices=DONATION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,
                                 help_text="Для денежных пожертвований")
    description = models.TextField(blank=True)
    is_anonymous = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.donation_type} от {self.name if not self.is_anonymous else 'Анонимно'}"


class GalleryImage(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='gallery/')
    location = models.ForeignKey(GreenLocation, on_delete=models.SET_NULL, related_name='images', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title