from django.db import models
from tinymce.models import HTMLField
from autoslug import AutoSlugField
import os
import uuid
def user_image_upload_path(instance, filename):
    # Get file extension
    ext = filename.split('.')[-1]
    # Generate unique filename
    new_filename = f"{uuid.uuid4()}.{ext}"
    # Return new file path
    return os.path.join('blogs_image/', new_filename)

class Blogs(models.Model):
    class Meta:
        verbose_name_plural = "Blog List"
    title = models.CharField(max_length=256)
    slug = AutoSlugField(populate_from='title',unique=True,null=True)
    description = HTMLField()
    image = models.FileField(upload_to=user_image_upload_path,max_length=250,null=True,default=None)
    