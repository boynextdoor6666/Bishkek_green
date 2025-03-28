# Generated by Django 5.1.7 on 2025-03-18 08:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('donation_type', models.CharField(choices=[('money', 'Денежная помощь'), ('trees', 'Саженцы'), ('materials', 'Материалы'), ('volunteer', 'Волонтёрство')], max_length=20)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, help_text='Для денежных пожертвований', max_digits=10, null=True)),
                ('description', models.TextField(blank=True)),
                ('is_anonymous', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='GreenLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('address', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('planned', 'Запланировано'), ('in_progress', 'В процессе'), ('completed', 'Завершено')], default='planned', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('area_size', models.PositiveIntegerField(blank=True, help_text='Размер территории в кв.м', null=True)),
                ('trees_planted', models.PositiveIntegerField(default=0)),
                ('image', models.ImageField(blank=True, null=True, upload_to='locations/')),
                ('is_featured', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='TreeType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='tree_types/')),
            ],
        ),
        migrations.CreateModel(
            name='GalleryImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('image', models.ImageField(upload_to='gallery/')),
                ('is_featured', models.BooleanField(default=False)),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='images', to='core.greenlocation')),
            ],
        ),
        migrations.CreateModel(
            name='PlantingRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=255)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[('pending', 'На рассмотрении'), ('approved', 'Одобрено'), ('rejected', 'Отклонено'), ('completed', 'Выполнено')], default='pending', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('admin_notes', models.TextField(blank=True)),
                ('preferred_tree_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.treetype')),
            ],
        ),
    ]
