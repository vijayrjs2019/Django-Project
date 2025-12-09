from django.contrib import admin
from .models import ContactUs

# Contact Us admin
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('name','email','phone_no','subject','message','created_at')

    # Disable editing
    def has_change_permission(self, request, obj =None):
        return False
    
    # Disable adding
    def has_add_permission(self, request):
        return False

admin.site.register(ContactUs,ContactUsAdmin)
