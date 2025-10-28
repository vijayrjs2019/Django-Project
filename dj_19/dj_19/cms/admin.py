from django.contrib import admin
from .models import CMS 

# Register your models here.
class CMSAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created_at', 'updated_at')
    search_fields = ('title', 'content') 
    ordering = ('-created_at',) 
    
    def has_add_permission(self, request):
        return False  # Disables "Add" button

    def has_delete_permission(self, request, obj=None):
        return False  # Disables deletion

admin.site.register(CMS, CMSAdmin)