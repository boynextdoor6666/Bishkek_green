from django.contrib import admin
from .models import TreeType, GreenLocation, PlantingRequest, Donation, GalleryImage


@admin.register(TreeType)
class TreeTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(GreenLocation)
class GreenLocationAdmin(admin.ModelAdmin):
    list_display = ('title', 'address', 'status', 'trees_planted', 'created_at', 'is_featured')
    list_filter = ('status', 'is_featured')
    search_fields = ('title', 'address', 'description')
    list_editable = ('status', 'is_featured')
    date_hierarchy = 'created_at'

    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'status', 'is_featured')
        }),
        ('Расположение', {
            'fields': ('address', 'latitude', 'longitude')
        }),
        ('Информация об озеленении', {
            'fields': ('area_size', 'trees_planted', 'image')
        }),
    )


@admin.register(PlantingRequest)
class PlantingRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'email', 'address', 'description')
    list_editable = ('status',)
    date_hierarchy = 'created_at'

    fieldsets = (
        (None, {
            'fields': ('name', 'email', 'phone', 'status')
        }),
        ('Информация о месте', {
            'fields': ('address', 'latitude', 'longitude', 'description', 'preferred_tree_type')
        }),
        ('Примечания', {
            'fields': ('admin_notes',)
        }),
    )


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'donation_type', 'amount', 'created_at')
    list_filter = ('donation_type', 'created_at', 'is_anonymous')
    search_fields = ('name', 'email', 'description')
    date_hierarchy = 'created_at'

    def display_name(self, obj):
        return 'Анонимно' if obj.is_anonymous else obj.name

    display_name.short_description = 'Имя'


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'is_featured', 'upload_date')
    list_filter = ('is_featured', 'upload_date')
    search_fields = ('title', 'description')
    list_editable = ('is_featured',)