from django.contrib import admin
from .models import Package

# 
# packages Models Admin
#   
class PackageAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'no_person', 'is_active', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    list_filter = ('is_active', 'created_at') 

    actions = ['make_active', 'make_inactive']

    @admin.action(description='Activate selected')
    def make_active(self, request, queryset):
        queryset.update(is_active=True)
    
    @admin.action(description='Deactivate selected')
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)

admin.site.register(Package, PackageAdmin)
