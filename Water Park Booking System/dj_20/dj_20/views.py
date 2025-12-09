from django.http import HttpResponse ,JsonResponse
from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from website_setting.models import Slider,GalleryImage,AboutUs,SiteInfo
from park_facilities.models import ParkFacility , ParkService , ParkTimings ,ParAttractions
from contact_us.models import ContactUs
from blogs.models import Blog , BlogComment
from packages.models import Package
from payment_settings.models import TaxInfo , Booking , RazorpaySettings
from cms.models import CMS  
from django.conf import settings
import json , razorpay
import uuid
from django.views.decorators.csrf import csrf_exempt
import random
from xhtml2pdf import pisa
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from django.db.models import Q

# Home Page
def home(request):
    package_list = Package.objects.all().order_by('-id')[:2]
    about_us_info = AboutUs.objects.first()
    slider_list=Slider.objects.all().order_by('-id')[:5]
    park_facility_list=ParkFacility.objects.filter(is_active=True).order_by('-id')[:3]
    park_service_list=ParkService.objects.filter(is_active=True).order_by('id')[:4]
    park_attractions_list=ParAttractions.objects.filter(is_active=True).order_by('id') 
    park_timings = ParkTimings.objects.all()
    gallery_image = GalleryImage.objects.all().order_by('id')[:6]
    return render(request,'pages/home.html',{'slider_list':slider_list,'park_facility_list':park_facility_list,'park_service_list':park_service_list,'park_timings':park_timings,'park_attractions_list':park_attractions_list,'gallery_image':gallery_image,'about_us_info':about_us_info,'package_list':package_list})

# About Us Page
def aboutUs(request):
    park_facility_list=ParkFacility.objects.filter(is_active=True).order_by('-id')[:3]
    gallery_image = GalleryImage.objects.all().order_by('id')[:6]
    about_us_info = AboutUs.objects.first()
    park_service_list=ParkService.objects.filter(is_active=True).order_by('id')[:4]
    return render(request,'pages/about.html',{'title':'About Us','subtitle':'About','gallery_image':gallery_image,'park_facility_list':park_facility_list,'about_us_info':about_us_info,'park_service_list':park_service_list})

# Service Page
def service(request):
    park_facility_list=ParkFacility.objects.all().order_by('-id')
    park_service_list=ParkService.objects.all().order_by('id')
    park_timings = ParkTimings.objects.all()
    return render(request,'pages/service.html',{'title':'Our Services','subtitle':'Service','park_facility_list':park_facility_list,'park_service_list':park_service_list,'park_timings':park_timings})

# Blog Page
def blog(request):
    blog_list = Blog.objects.all().order_by('-id')
    return render(request,'pages/blog.html',{'title':'Our Blog','subtitle':'Blog','blog_list':blog_list})    

# Contact Us Page
def contactUs(request):
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        user_email = request.POST.get('user_email')
        user_phone_no = request.POST.get('user_phone_no')
        user_subject = request.POST.get('user_subject')
        user_message = request.POST.get('user_message')

        if not user_name or not user_email or not user_phone_no or not user_subject or not user_message :
            messages.error(request, "All fields are required!")
        else :
            ContactUs.objects.create(
                name=user_name,
                email=user_email,
                phone_no=user_phone_no,
                subject=user_subject,
                message=user_message
            )
            messages.success(request, "Your enquiry has been successfully submitted!")
        return redirect('contactUs')

    return render(request,'pages/contact.html',{'title':'Contact Us','subtitle':'Contact'})

# Package Page
def package(request):
    package_list = Package.objects.all().order_by('-id')
    return render(request,'pages/package.html',{'title':'Ticket Packages','subtitle':'Packages','package_list':package_list}) 

# Gallery Page
def gallery(request):
    gallery_image = GalleryImage.objects.all().order_by('id')
    return render(request,'pages/gallery.html',{'title':'Our Gallery','subtitle':'Gallery','gallery_image':gallery_image}) 

# Feature Page
def feature(request):
    park_facility_list=ParkFacility.objects.filter(is_active=True).order_by('-id')
    return render(request,'pages/feature.html',{'title':'Our Features','subtitle':'Feature','park_facility_list':park_facility_list}) 

# Feature Details Page
def featureDetails(request, slug):
    park_facility_info=ParkFacility.objects.filter(slug=slug).first()
    return render(request,'pages/featureDetails.html',{'title':park_facility_info.title,'subtitle':park_facility_info.title,'park_facility_info':park_facility_info}) 

# Page Not Found
def pageNotFound(request):
    return render(request,'pages/404.html',{'title':'404 Pages','subtitle':'404 Page'})

# Blog Details Page
def blogDetails(request, slug):
    if request.method == 'POST':
        user_first_name = request.POST.get('first_name')
        user_last_name = request.POST.get('last_name')
        user_email = request.POST.get('user_email')
        user_message = request.POST.get('user_message')
        blog_id = request.POST.get('blog_id')

        if not user_first_name or not user_last_name or not user_email or not user_message :
            messages.error(request, "All fields are required!")
        else :
            BlogComment.objects.create(
                blog_id=blog_id,
                user_first_name=user_first_name,
                user_last_name=user_last_name,
                user_email=user_email,
                message=user_message
            )
            messages.success(request, "Your comment has been successfully submitted!")
        return redirect('blogDetails', slug=slug)
    
    blog_info=get_object_or_404(Blog, slug=slug)
    blog_comments = BlogComment.objects.filter(is_active=True,blog_id=blog_info.id).order_by('-id')
    return render(request,'pages/blogDetails.html',{'title':blog_info.title,'subtitle':blog_info.title,'blog_info':blog_info,'blog_comments':blog_comments})

def bookNow(request, id):
    package_info = get_object_or_404(Package, id=id)
    totalPrice = 0
    subTotal = totalPrice+package_info.price
    tax_information = TaxInfo.objects.filter(is_active=True).order_by('-id')
    for tax_item in tax_information:
        if tax_item.tex_apply_type == 'Flat':
            totalPrice += tax_item.tax_rate
        elif tax_item.tex_apply_type == 'Percentage':
            totalPrice += (subTotal * tax_item.tax_rate) / 100
    totalPrice = subTotal + totalPrice 
    return render(request,'pages/bookNow.html',{'title':'Book Now','subtitle':'Book Now','package_info':package_info,'tax_information':tax_information,'totalPrice':totalPrice})

def bookingConfirmation(request):
    if request.method == 'POST':
        booking_date = request.POST.get('booking_date')
        package_id = request.POST.get('package_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_no = request.POST.get('user_phone_no')
        user_email = request.POST.get('user_email')  

        if not first_name or not last_name or not user_email or not phone_no :
            messages.error(request, "All fields are required!")
            return redirect('bookNow', id=package_id)
        
    package_info = get_object_or_404(Package, id=package_id)
    totalPrice = 0
    subTotal = totalPrice+package_info.price
    tax_information = TaxInfo.objects.filter(is_active=True).order_by('-id')
    tax_list = []
    for tax_item in tax_information:
        if tax_item.tex_apply_type == 'Flat':
            totalPrice += tax_item.tax_rate
        elif tax_item.tex_apply_type == 'Percentage':
            totalPrice += (subTotal * tax_item.tax_rate) / 100
        tax_list.append({
            "type": tax_item.tex_apply_type,
            "rate": float(tax_item.tax_rate)
        })
        tax_json = json.dumps(tax_list)

    totalPrice = subTotal + totalPrice

    return render(request,'pages/payNow.html',{'title':'Booking Confirmation','subtitle':'Booking Confirmation','package_id':package_id,'first_name':first_name,'last_name':last_name,'phone_no':phone_no,'user_email':user_email,'submitte_totalPrice':totalPrice,'package_info':package_info,'tax_information':tax_information,'totalPrice':totalPrice,'tax_json':tax_json,'booking_date':booking_date})


@csrf_exempt
def payNow(request):
    if request.method == 'POST':
       order_id = random.randint(1000, 9999)
       booking_id = f"WTL-{uuid.uuid4().hex[:8].upper()}"
       payment_id = ''
       payment_status = 'Pending'

       data = request.POST 
       package_id = data.get('package_id')
       totalPrice = data.get('totalPrice')
       submitte_totalPrice = data.get('submitte_totalPrice')
       tax_details = data.get('tax_details')
       userData = json.loads(request.POST.get('userData'))
       first_name = userData.get('first_name')
       last_name = userData.get('last_name') 
       phone_no = userData.get('phone_no')
       user_email = userData.get('user_email')
       booking_date = userData.get('booking_date')
       tax_details = userData.get('tax_details')
       inserted_id = ""

       package_info = get_object_or_404(Package, id=package_id)
       # Save Booking Data
       bookingData = Booking.objects.create(
            Booking_id=booking_id,
            payment_id=payment_id, 
            payment_status=payment_status, 
            first_name=first_name, 
            last_name=last_name,
            phone_no=phone_no,
            user_email=user_email,
            sub_total_price=totalPrice,
            total_price=submitte_totalPrice,
            tax_info=tax_details,
            package_title=package_info.title,
            package_description=package_info.description,
            price=package_info.price,
            no_person=package_info.no_person,
            booking_date=booking_date
        )
       
       inserted_id = bookingData.id
       # Get Razorpay Setting
    razorpaySetting = RazorpaySettings.objects.first()
    payment_id = str(order_id)+str(inserted_id)
    amount_paise = int(float(submitte_totalPrice) * 100)
    client = razorpay.Client(auth=(razorpaySetting.key_id, razorpaySetting.key_secret))
    # Create Razorpay order
    razorpay_order = client.order.create({
        "amount": amount_paise,
        "currency": "INR",
        "receipt": f"order_rcptid_{payment_id}",
        "payment_capture": 1
    })
    bookingData.payment_id = razorpay_order['id']
    bookingData.save()
    return JsonResponse({
                'success': True, 
                'payment_id': razorpay_order['id'], 
                'razorpay_key_id': razorpaySetting.key_id,
                'amount': submitte_totalPrice,
                'success_url': '/payment-success',
                'booking_id': inserted_id,
                'gateway_mode': razorpaySetting.gateway_mode
            }, status=200)

    return JsonResponse({'status': 'error'}, status=400)

# Razorpay Success
@csrf_exempt
@require_POST
def razorpaySuccess(request):
    try:
        data = json.loads(request.body)
        booking_id = data.get('booking_id')
        if not booking_id:
            return JsonResponse({"error": "Missing booking ID."}, status=400)
        try:
            bookingData = Booking.objects.get(id=booking_id)
            bookingData.payment_status = 'Completed'
            bookingData.save()
            return JsonResponse({
                "redirect_url": "/payment-success/" + str(booking_id),
                "message": "Payment successful and booking confirmed."
            })
        except Booking.DoesNotExist:
            return JsonResponse({"error": "Booking not found."}, status=404)

    except Exception as e:
        print("Error in razorpaySuccess:", e)
        return JsonResponse({"error": str(e)}, status=500)
    
def paymentSuccess(request,id):
    bookingData = Booking.objects.get(id=id)
    return render(request,'pages/payment-success.html',{'title':'Thank you','subtitle':'Thank you','bookingData':bookingData})


def downloadReceiptPDF(request,id):
    siteData = SiteInfo.objects.first()
    bookingData = Booking.objects.get(id=id) 
    taxAmount = 0
    taxAmount = float(bookingData.total_price) - float(bookingData.price)
    bookingData.tax_amount = taxAmount
    context = {
        "siteData": siteData,
        "bookingData": bookingData,  
        "tax_amount": taxAmount,
    }
    html = render_to_string("pages/receipt_pdf.html", context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="receipt.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("Error creating PDF", status=500)

    return response

def findReceipt(request):
    if request.method == 'POST':
        find_id = request.POST.get('find_id')
        try:
            bookingData = Booking.objects.get(
                Q(payment_id=find_id) | Q(Booking_id=find_id)
            )
            return redirect('paymentSuccess', id=bookingData.id)

        except Booking.DoesNotExist:
            messages.error(request, "No receipt found for the provided Payment/Booking ID.")
            return redirect('findReceipt')

        except Booking.MultipleObjectsReturned:
            # In case more than one result is found, pick the first record
            bookingData = Booking.objects.filter(
                Q(payment_id=find_id) | Q(Booking_id=find_id)
            ).first()
            return redirect('paymentSuccess', id=bookingData.id)
        
    return render(request,'pages/find-receipt.html',{'title':'Find Receipt','subtitle':'Find Receipt'})

def contentInfo(request, slug): 
    try:
        content = CMS.objects.get(slug=slug)
        return render(request,'pages/contentInfo.html',{'title': content.title, 'subtitle':content.title,'content': content})
    except CMS.DoesNotExist:
        # If the CMS content does not exist, redirect to a 404 page or handle it accordingly
        return render(request, 'pages/404.html',{'title': '404 Pages', 'subtitle':'404 Pages'})