from django.db import models
from tinymce.models import HTMLField
from autoslug import AutoSlugField
# Create your models here.
class CMS(models.Model):
    title = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='title',unique=True,null=True)
    content = HTMLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Content Management System'
        verbose_name_plural = 'Content Management Systems'
        ordering = ['-created_at']  # Order by creation date, newest first