from django.urls import path
from . import views

urlpatterns = [
    path('', views.gallery),
    path('upload/', views.upload_photo, name='upload'),
    path('gallery/', views.gallery, name='gallery'),
    path('qr/<str:target>/', views.generate_qr, name='generate_qr'),
    path('qr-page/', views.qr_page, name='qr_page'),
    path('delete/<int:photo_id>/', views.delete_photo, name='delete_photo'),

]
