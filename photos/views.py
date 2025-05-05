from django.shortcuts import render, redirect
from .models import Photo
import qrcode
from io import BytesIO
from django.http import HttpResponse
from .cloudinary_init import *
import base64
from cloudinary.uploader import destroy
from django.shortcuts import get_object_or_404

from cloudinary.uploader import upload as cloudinary_upload

def upload_photo(request):
    if request.method == 'POST':
        image = request.FILES.get('photo')
        caption = request.POST.get('caption', '')

        if not image:
            return render(request, 'upload.html', {'error': 'No image uploaded'})

        # Upload to Cloudinary manually to get public_id
        result = cloudinary_upload(image)       
        photo = Photo.objects.create(
        image_url=result['secure_url'],  # ✅ This matches your model now
        public_id=result['public_id'],
        caption=caption
        )



        return redirect('gallery')

    return render(request, 'upload.html')


def gallery(request):
    all_photos = Photo.objects.all()

    # Only keep photos that have a valid Cloudinary URL
    valid_photos = [photo for photo in all_photos if photo.image_url and 'res.cloudinary.com' in photo.image_url]

    return render(request, 'gallery.html', {'photos': valid_photos})


def generate_qr(request, target='upload'):
    if target not in ['upload', 'gallery']:
        target = 'upload'

    # Replace with your PC’s local IP address
    ip_address = '192.168.2.24'
    url = f'http://{ip_address}:8000/{target}/'

    qr_img = qrcode.make(url)
    buffer = BytesIO()
    qr_img.save(buffer, format='PNG')
    buffer.seek(0)

    return HttpResponse(buffer.getvalue(), content_type='image/png')

def qr_page(request):
    upload_url = request.build_absolute_uri('/upload/')

    # Generate QR Code in memory
    qr = qrcode.make(upload_url)
    buffer = BytesIO()
    qr.save(buffer, format='PNG')
    qr_image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return render(request, 'qr_page.html', {'qr_image_base64': qr_image_base64, 'upload_url': upload_url})


def delete_photo(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)

    # Delete from Cloudinary
    if photo.public_id:
        destroy(photo.public_id)

    # Delete from database
    photo.delete()

    return redirect('gallery')

