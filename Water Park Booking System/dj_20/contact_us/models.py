from django.db import models

# 
# Contact Us
# 
class ContactUs(models.Model):
    name = models.CharField(max_length=200, verbose_name='User Name')
    email = models.CharField(max_length=200, verbose_name='User Email')
    phone_no = models.CharField(max_length=15, verbose_name='User phone no')
    subject = models.CharField(max_length=200, verbose_name='Subject')
    message = models.TextField(verbose_name='Message', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
      
    class Meta:
        verbose_name = 'Contact Us'
        verbose_name_plural = 'Contact Us'
        ordering = ['-created_at']  # Order by upload date descending
