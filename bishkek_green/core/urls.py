from django.urls import path
from . import views

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

    # API для карты
    path('api/locations/', views.locations_json, name='locations_json'),
    path('api/requests/', views.requests_json, name='requests_json'),
]