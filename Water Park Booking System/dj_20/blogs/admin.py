from django.contrib import admin
from django.utils.html import format_html
from .models import Blog , BlogCategory ,BlogComment

# 
# Register Blog model in admin site
# 
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title','blogCategory', 'is_active', 'created_at', 'updated_at')
    search_fields = ('title',)
    list_filter = ('is_active', 'created_at') 

    actions = ['make_active', 'make_inactive']

    @admin.action(description='Activate selected')
    def make_active(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description='Deactivate selected')
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "-"
    image_tag.short_description = 'Image'

admin.site.register(Blog,BlogAdmin)

# 
# Blog Category Admin
# 
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('is_active', 'created_at') 

    actions = ['make_active', 'make_inactive']

    @admin.action(description='Activate selected')
    def make_active(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description='Deactivate selected')
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)

admin.site.register(BlogCategory,BlogCategoryAdmin)

# 
# Register Blog Comment model in admin site
# 
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ('blog', 'user_first_name', 'user_last_name', 'user_email', 'is_active','created_at', 'updated_at')
    search_fields = ('user_email', 'blog__title')
    list_filter = ('created_at','is_active')

    actions = ['make_active', 'make_inactive']

    @admin.action(description='Activate selected')
    def make_active(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description='Deactivate selected')
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)

admin.site.register(BlogComment,BlogCommentAdmin)