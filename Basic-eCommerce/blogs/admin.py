from django.contrib import admin
from .models import Blogs
from django.utils.html import format_html , strip_tags

class BlogsAdmin(admin.ModelAdmin):
    list_display = ('title','image_tag','clean_strip_tags')

    def image_tag(self,obj):
        if obj.image :
            return format_html('<img src="{}" width="50" height="50" />',obj.image.url)
        return "-"
    image_tag.short_description = 'Image'

    def clean_strip_tags(self,obj):
        if obj.description:
            return strip_tags(obj.description)
        return "-"
    clean_strip_tags.short_description = 'Description'

admin.site.register(Blogs,BlogsAdmin)
