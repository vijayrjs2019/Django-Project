from django.contrib import admin
from .models import BookingList
# Register your models here.
class BookingListAdmin(admin.ModelAdmin):
    list_display = ('order_id','payment_id','name', 'email', 'phone_no', 'departure_date','destination', 'country', 'duration', 'no_person', 'hotel_type', 'booking_type', 'payment_status', 'created_at', 'is_active')
    search_fields = ('name',)  

    # Disable editing existing entries
    def has_change_permission(self, request, obj=None):
        return False

    # Disable adding new entries
    def has_add_permission(self, request):
        return False

admin.site.register(BookingList,BookingListAdmin)
