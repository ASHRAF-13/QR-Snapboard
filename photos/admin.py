from django.contrib import admin
from django.contrib import admin
from .models import Photo

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('caption', 'image_url', 'public_id', 'uploaded_at')

# Register your models here.
