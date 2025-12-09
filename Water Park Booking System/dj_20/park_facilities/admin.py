from django.contrib import admin
from django.utils.html import format_html
from .models import ParkFacility ,ParkService, ParkTimings ,ParAttractions

# ParkFacility Admin
class ParkFacilityAdmin(admin.ModelAdmin):
    list_display = ('title', 'image_tag','created_at', 'updated_at','is_active')
    
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

admin.site.register(ParkFacility, ParkFacilityAdmin)

# ParkService Admin
class ParkServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at','is_active')
    
    actions = ['make_active', 'make_inactive']

    @admin.action(description='Activate selected')
    def make_active(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description='Deactivate selected')
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)

admin.site.register(ParkService, ParkServiceAdmin)

# ParkTimings Admin
class ParkTimingsAdmin(admin.ModelAdmin):
    list_display = ('day', 'opening_time', 'closing_time','created_at', 'updated_at','is_active')
    
    actions = ['make_active', 'make_inactive']

    @admin.action(description='Activate selected')
    def make_active(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description='Deactivate selected')
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
        
admin.site.register(ParkTimings, ParkTimingsAdmin)


# Park Attractions Admin
class ParkAttractionsAdmin(admin.ModelAdmin):
    list_display = ('title', 'image_tag','created_at', 'updated_at','is_active')
    
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

admin.site.register(ParAttractions, ParkAttractionsAdmin)