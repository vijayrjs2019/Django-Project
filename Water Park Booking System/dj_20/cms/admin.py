from django.contrib import admin
from .models import CMS
# Register your models here.

class CMSAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_active', 'created_at', 'updated_at') 
    search_fields = ('title', 'content') 
    ordering = ('-id',)

    actions = ['make_active', 'make_inactive']

    @admin.action(description='Activate selected')
    def make_active(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description='Deactivate selected')
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)

admin.site.register(CMS,CMSAdmin)
