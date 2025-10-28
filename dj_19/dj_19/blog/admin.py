from django.contrib import admin
from .models import Blog
from django.utils.html import format_html,strip_tags

# Register your models here.
class BlogAdmin(admin.ModelAdmin): 
    list_display = ('title', 'image_tag', 'created_at', 'updated_at', 'is_active')
    search_fields = ('title',) 
    actions = ['make_active', 'make_inactive']

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px;"/>', obj.image.url)
        return "No Image"
    
    image_tag.short_description = 'Image' 

    @admin.action(description="Mark selected blogs as Active")
    def make_active(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "Selected blogs marked as Active.")

    @admin.action(description="Mark selected blogs as Inactive")
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "Selected blogs marked as Inactive.")

admin.site.register(Blog, BlogAdmin)
# Register the Blog model with the custom admin interface