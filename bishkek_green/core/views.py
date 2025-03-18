from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import models
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import GreenLocation, PlantingRequest, TreeType, GalleryImage, Donation
from .forms import PlantingRequestForm, DonationForm, ContactForm, RegistrationForm
import logging
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect

class CustomLogoutView(auth_views.LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, 'Вы успешно вышли из системы.')
        return super().dispatch(request, *args, **kwargs)

    # Разрешить GET-запросы для выхода
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


def index(request):
    """Главная страница"""
    total_locations = GreenLocation.objects.count()
    total_trees = GreenLocation.objects.aggregate(sum=models.Sum('trees_planted'))['sum'] or 0
    featured_locations = GreenLocation.objects.filter(is_featured=True)[:3]
    recent_plantings = GreenLocation.objects.filter(status='completed').order_by('-updated_at')[:3]
    featured_images = GalleryImage.objects.filter(is_featured=True)[:5]

    context = {
        'total_locations': total_locations,
        'total_trees': total_trees,
        'featured_locations': featured_locations,
        'recent_plantings': recent_plantings,
        'featured_images': featured_images,
    }
    return render(request, 'index.html', context)


def green_map(request):
    """Страница с интерактивной картой"""
    context = {
        'center_lat': 42.8746,  # Центр Бишкека
        'center_lng': 74.5698,
        'zoom': 12
    }
    return render(request, 'map.html', context)


@login_required(login_url='/accounts/login/')  # Используйте полный путь
def planting_request(request):
    if request.method == 'POST':
        form = PlantingRequestForm(request.POST)
        if form.is_valid():
            planting_request = form.save(commit=False)
            planting_request.user = request.user
            lat = request.POST.get('hidden_lat')
            lng = request.POST.get('hidden_lng')

            if lat and lng:
                planting_request.latitude = float(lat)
                planting_request.longitude = float(lng)
            planting_request.save()

            messages.success(request, 'Ваша заявка успешно отправлена! Мы свяжемся с вами в ближайшее время.')
            return redirect('core:success')
    else:
        form = PlantingRequestForm()

    context = {
        'form': form,
        'tree_types': TreeType.objects.all(),
    }
    return render(request, 'submit_location.html', context)


def donate(request):
    """Страница пожертвований"""
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Спасибо за вашу поддержку! Вместе мы делаем Бишкек зеленее.')
            return redirect('core:success')
    else:
        form = DonationForm()

    recent_donors = Donation.objects.filter(is_anonymous=False).order_by('-created_at')[:5]

    context = {
        'form': form,
        'recent_donors': recent_donors,
    }
    return render(request, 'donate.html', context)


def about(request):
    """Страница о фонде"""
    context = {
        'tree_types': TreeType.objects.all(),
        'completed_projects': GreenLocation.objects.filter(status='completed').count(),
    }
    return render(request, 'about.html', context)


def contact(request):
    """Страница контактов"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Ваше сообщение успешно отправлено!')
            return redirect('core:success')
    else:
        form = ContactForm()

    context = {
        'form': form,
    }
    return render(request, 'contact.html', context)


def gallery(request):
    """Галерея проекта"""
    images = GalleryImage.objects.all().order_by('-upload_date')
    paginator = Paginator(images, 12)  # 12 изображений на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'gallery.html', context)


def success(request):
    """Страница успешной отправки формы"""
    return render(request, 'success.html')


def locations_json(request):
    """API для получения всех локаций для карты"""
    locations = GreenLocation.objects.all()
    data = []

    for loc in locations:
        data.append({
            'id': loc.id,
            'title': loc.title,
            'description': loc.description,
            'lat': loc.latitude,
            'lng': loc.longitude,
            'status': loc.status,
            'trees_planted': loc.trees_planted,
            'image': loc.image.url if loc.image else None,
        })

    return JsonResponse({'locations': data})


def requests_json(request):
    """API для получения одобренных заявок для карты"""
    requests = PlantingRequest.objects.filter(status='approved', latitude__isnull=False)
    data = []

    for req in requests:
        data.append({
            'id': req.id,
            'address': req.address,
            'description': req.description,
            'lat': req.latitude,
            'lng': req.longitude,
        })

    return JsonResponse({'requests': data})


logger = logging.getLogger(__name__)
def register(request):
    """Регистрация пользователя"""
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            logger.info(f'User {user.username} registered successfully.')
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('core:index')
        else:
            logger.error(f'Form errors: {form.errors}')  # Логирование ошибок формы
            messages.error(request, 'Ошибка при регистрации. Проверьте введенные данные.')
    else:
        form = RegistrationForm()

    return render(request, 'registration/register.html', {'form': form})