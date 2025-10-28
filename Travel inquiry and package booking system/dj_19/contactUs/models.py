from django.db import models

# User Enquiry
class UserEnquiry(models.Model):
    class Meta:
        verbose_name_plural = "User Enquiry"
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=150)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

# Subscribe List
class Subscribers(models.Model):
    class Meta:
        verbose_name_plural = 'Newsletter Subscribes'
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
