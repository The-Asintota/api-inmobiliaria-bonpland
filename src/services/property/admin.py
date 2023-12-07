from django.contrib import admin
from .models import Home, Department, Local


class HomeAdminPanel(admin.ModelAdmin):
    list_display=[field.name for field in Home._meta.get_fields()]
    search_fields=['id', 'date_joined', 'location']
    list_filter=['availability_type', 'rooms', 'bathrooms', 'garages', 'floors', 'garden']


class DepartmentAdminPanel(admin.ModelAdmin):
    list_display=[field.name for field in Department._meta.get_fields()]
    search_fields=['id', 'date_joined', 'location']
    list_filter=['availability_type', 'rooms','bathrooms', 'floors']


class LocalAdminPanel(admin.ModelAdmin):
    list_display=[field.name for field in Local._meta.get_fields()]
    search_fields=['id', 'date_joined', 'location']
    list_filter=['availability_type', 'type_local', 'parking_lot']


admin.site.register(Home, HomeAdminPanel)
admin.site.register(Department, DepartmentAdminPanel)
admin.site.register(Local, LocalAdminPanel)