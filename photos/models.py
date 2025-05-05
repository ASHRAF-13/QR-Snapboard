from django.db import models
from cloudinary_storage.storage import MediaCloudinaryStorage
from django.db import models

class Photo(models.Model):
    image_url = models.URLField(blank=True, null=True)
    caption = models.CharField(max_length=255, blank=True)
    public_id = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)


# Create your models here.
