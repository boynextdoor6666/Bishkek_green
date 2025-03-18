from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('map/', views.green_map, name='map'),
    path('request/', views.planting_request, name='planting_request'),
    path('donate/', views.donate, name='donate'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('gallery/', views.gallery, name='gallery'),
    path('success/', views.success, name='success'),
    path('accounts/', include('django.contrib.auth.urls')),  # Стандартные пути для аутентификации
    path('accounts/register/', views.register, name='register'),  # Кастомный путь для регистрации

    # API для карты
    path('api/locations/', views.locations_json, name='locations_json'),
    path('api/requests/', views.requests_json, name='requests_json'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)