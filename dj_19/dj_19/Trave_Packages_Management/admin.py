from django.contrib import admin , messages
from django.utils.html import format_html , mark_safe
from django.urls import reverse , path
from django.shortcuts import render, get_object_or_404 ,  redirect
from .models import TravelPackage , TravelEnquiry , QuotationInfo
from .forms import SendQuotationForm   
# Register your models here.
class TravelPackageAdmin(admin.ModelAdmin):
    list_display = ('package_name','category','destination', 'country', 'price', 'offer_price', 'formatted_duration', 'no_person', 'hotel_type_display', 'is_active', 'created_at')
    search_fields = ('package_name', 'destination','category__category_name', 'country__country_name')
    ordering = ('-created_at',)
    actions = ['make_active', 'make_inactive']

    def hotel_type_display(self, obj):
        return obj.get_hotel_type_display()
    hotel_type_display.short_description = 'Hotel Type'

    def formatted_duration(self, obj):
        day_str = "day" if obj.duration == 1 else "days"
        return f"{obj.duration} {day_str}"
    formatted_duration.short_description = 'Duration'

    @admin.action(description="Mark selected package as Active")
    def make_active(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "Selected package marked as Active.")

    @admin.action(description="Mark selected package as Inactive")
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "Selected package marked as Inactive.")

admin.site.register(TravelPackage, TravelPackageAdmin)   

class TravelEnquiryAdmin(admin.ModelAdmin):
    list_display = ('name','email','phone_no','departure_date','no_person','hotel_type','destination','country', 'get_user_display','is_active', 'created_at','send_quotation_button')
    ordering = ('-created_at',)
    actions = ['make_active', 'make_inactive']

    def has_add_permission(self, request):
        return True  # ✅ allow adding

    def has_change_permission(self, request, obj=None):
        return False  # ❌ disallow editing

    def has_delete_permission(self, request, obj=None):
        return True  # ✅ allow deleting

    def has_view_permission(self, request, obj=None):
        return True  # ✅ allow viewing
    
    @admin.display(description='User')
    def get_user_display(self, obj):
        return obj.user.username if obj.user else 'Guest'

    @admin.action(description="Mark selected Enquiry as Active")
    def make_active(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "Selected Enquiry marked as Active.")

    @admin.action(description="Mark selected Enquiry as Inactive")
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "Selected Enquiry marked as Inactive.")

    @admin.display(description='Send/View Quotation')
    def send_quotation_button(self, obj):
        quotation_exists = obj.travelEnquiry_quotationInfo.exists()
        if quotation_exists:
            # Show "View Quotation" button
            view_url = reverse('admin:view_quotation', args=[obj.pk])  # You define this view
            return format_html('<a class="button" href="{}" style="background-color: #28a745;">View Quotation</a>', view_url)
        else:
            # Show "Send Quotation" button
            send_url = reverse('admin:send_quotation', args=[obj.pk])
            return format_html('<a class="button" href="{}" style="background-color: #007bff;">Send Quotation</a>', send_url)

    
    # Set path of button
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'send-quotation/<int:enquiry_id>/',
                self.admin_site.admin_view(self.send_quotation_view),
                name='send_quotation',
            ),
            path(
                'view-quotation/<int:enquiry_id>/',
                self.admin_site.admin_view(self.display_quotation_list),
                name='view_quotation',
            ),
        ]
        return custom_urls + urls

    # Insert Data / view form
    def send_quotation_view(self, request, enquiry_id):
        enquiry = get_object_or_404(TravelEnquiry, pk=enquiry_id)

        if request.method == 'POST':
            form = SendQuotationForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                details = form.cleaned_data['details']

                # 🔽 Save to QuotationInfo model
                QuotationInfo.objects.create(
                    travelEnquiry=enquiry,
                    quotation_amount="{:.2f}".format(float(amount)),  # Format float to 2 decimal places
                    quotation_deacription=details,
                    user=request.user,
                    is_active=True
                )

                messages.success(request, f"Quotation of ₹{amount} sent successfully for {enquiry.name}.")
                return redirect(reverse('admin:Trave_Packages_Management_travelenquiry_changelist'))
        else:
            form = SendQuotationForm()

        context = {
            'title': f"Send Quotation for: {enquiry.name}",
            'form': form,
            'enquiry': enquiry,
            'opts': self.model._meta,
            'original': enquiry,
            'has_permission': True,
        }
        return render(request, 'admin/send_quotation_form.html', context)
    
    # view quotation view By Inquery ID
    def display_quotation_list(self, request, enquiry_id):
        enquiry = get_object_or_404(TravelEnquiry, pk=enquiry_id) 
        quotationlist = QuotationInfo.objects.filter(travelEnquiry=enquiry).first()

        context = {
            'title': f"Send Quotation for: {enquiry.name}", 
            'enquiry': enquiry,
            'quotationlist':quotationlist,
            'opts': self.model._meta,
            'original': enquiry,
            'has_permission': True,
        }
        return render(request, 'admin/quotation_list.html', context)


    
admin.site.register(TravelEnquiry, TravelEnquiryAdmin)   


class QuotationInfoAdmin(admin.ModelAdmin):
    list_display = ('quotation_amount','quotation_deacription', 'user', 'created_at') 

admin.site.register(QuotationInfo, QuotationInfoAdmin)  