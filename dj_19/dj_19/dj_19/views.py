from django.http import HttpResponse ,JsonResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from cms.models import CMS
from django.db.models import Count , Q
from setting.models import Setting, SocialMediaLink , AboutUs , Slider ,OurGallery,Categories,Countries
from jobs.models import Jobs,ReceiveJobApplication
from blog.models import Blog,BlogComment
from travelGuides.models import TravelGuide , Testimonial ,OurServices 
from contactUs.models import UserEnquiry , Subscribers
from collections import defaultdict
from Trave_Packages_Management.models import TravelPackage , TravelEnquiry ,QuotationInfo
from django.contrib.auth.forms import UserCreationForm
from authUsers.forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout , update_session_auth_hash
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from authUsers.models import UserProfile
from django.utils.text import slugify
from django.contrib.auth.models import User
from TaxAndGateway.models import TaxSetting , RazorpaySetting
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from bookings.models import BookingList 
import random
import razorpay
from django.conf import settings
from django.views.decorators.http import require_POST
from django.core.serializers.json import DjangoJSONEncoder
import json 
from xhtml2pdf import pisa
from django.template.loader import render_to_string
from django.urls import reverse
from django.db.models import Count, Sum, Case, When, IntegerField, FloatField
# Create your views here.
@never_cache
def home(request):
    # Category
    categoriesList = Categories.objects.filter(is_active=True).order_by('category_name')
    # Gallery
    our_gallery = OurGallery.objects.filter(is_active=True).order_by('-created_at')[:10]
    # Slider
    sliderList = Slider.objects.filter(is_active=True).order_by('-created_at')[:3]
    # About Us Info
    aboutUsInfo = AboutUs.objects.first()
    # Services
    ourServices = OurServices.objects.filter(is_active=True).order_by('-created_at')[:6]
    total = ourServices.count()
    half = (total + 1) // 2 
    left_ourServices = ourServices[:half]
    right_ourServices = ourServices[half:]
    # Testimonials
    testimonials = Testimonial.objects.filter(is_active=True).order_by('-created_at')[:6]
    # Resent Blog
    resentBlogs = Blog.objects.filter(is_active=True).annotate(total_comments=Count('comments', filter=Q(comments__is_active=True))).order_by('-created_at')[:3] 
    # Guide
    otherGuide = TravelGuide.objects.filter(is_active=True).order_by('-created_at')[:4]
    # travel_packages
    travel_packages = TravelPackage.objects.filter(is_active=True).order_by('-created_at')[:12]
    # tour_list
    tour_list = Categories.objects.filter(is_active=True).order_by('category_name')[:6] 
    # country list
    country_list= Countries.objects.filter(is_active=True).order_by('country_name')
    # Popular Destination
    grouped_by_country = defaultdict(lambda: {
        'count': 0,
        'latest_image': None,
        'images': [],
    })
    popular_destination = OurGallery.objects.filter(is_active=True).select_related('country').order_by('-created_at')
    for img in popular_destination:
        country = img.country.name if hasattr(img.country, 'name') else img.country  # handle FK or CharField
        grouped_by_country[country]['images'].append(img)
        grouped_by_country[country]['count'] += 1
        if grouped_by_country[country]['latest_image'] is None:
            grouped_by_country[country]['latest_image'] = img 
    return render(request, 'pages/home.html',{'title': 'Home','breadcrumb_title': 'Home','otherGuide':otherGuide,'resentBlogs':resentBlogs,'testimonials':testimonials,'left_ourServices':left_ourServices,'right_ourServices':right_ourServices,'aboutUsInfo':aboutUsInfo,'sliderList':sliderList,'categoriesList':categoriesList,'our_gallery':our_gallery,'travel_packages':travel_packages,'tour_list':tour_list,'country_list':country_list,'grouped_by_country':dict(grouped_by_country)}) 

def about(request):
    about_us = AboutUs.objects.first()
    otherGuide = TravelGuide.objects.filter(is_active=True).order_by('-created_at')[:4]
    if not about_us:
        messages.error(request, "About Us content is not available.")
        return redirect('home')
    return render(request, 'pages/about.html',{'title': 'About','breadcrumb_title': 'About Us','about_us':about_us,'otherGuide':otherGuide})

def services(request):
    ourServices = OurServices.objects.filter(is_active=True).order_by('-created_at')[:12]
    total = ourServices.count()
    half = (total + 1) // 2 
    left_ourServices = ourServices[:half]
    right_ourServices = ourServices[half:]
    testimonials = Testimonial.objects.filter(is_active=True).order_by('-created_at')[:6]
    return render(request, 'pages/services.html',{'title': 'Services','breadcrumb_title': 'Our Services','testimonials':testimonials,'left_ourServices':left_ourServices,'right_ourServices':right_ourServices})

def packages(request, category_id=None):
    if category_id:
        travel_packages = TravelPackage.objects.filter(category_id=category_id).order_by('-created_at')[:12]
    else:
        travel_packages = TravelPackage.objects.filter(is_active=True).order_by('-created_at')[:12]

    total = travel_packages.count()
    return render(request, 'pages/packages.html',{'title': 'Packages','breadcrumb_title': 'Travel Packages','travel_packages':travel_packages,'total':total })

def blog(request):
    blogs = Blog.objects.filter(is_active=True).annotate(total_comments=Count('comments', filter=Q(comments__is_active=True))).order_by('-created_at')
    return render(request, 'pages/blog.html',{'title': 'Blog','breadcrumb_title': 'Our Blog','blogs': blogs})

def contact(request):
    websiteData = Setting.objects.first()
    return render(request, 'pages/contact.html',{'title': 'Contact','breadcrumb_title': 'Contact Us','websiteData': websiteData})

def generate_unique_username(first_name, last_name):
    base_username = slugify(f"{first_name}{last_name}")
    username = base_username
    counter = 1
    while User.objects.filter(username=username).exists():
        username = f"{base_username}{counter}"
        counter += 1
    return username


def booking(request,package_id=None):

    if request.method == 'POST':
        bon_name = request.POST.get('bon_name')
        bon_email = request.POST.get('bon_email')
        bon_phone = request.POST.get('bon_phone') 
        bon_departure_date = request.POST.get('bon_departure_date') 
        bon_no_person = request.POST.get('bon_no_person') 
        bon_hotel_type = request.POST.get('bon_hotel_type') 
        bon_category = request.POST.get('bon_category') 
        bon_destination = request.POST.get('bon_destination') 
        bon_country = request.POST.get('bon_country')
        bon_duration = request.POST.get('bon_duration')
        bon_tour_details = request.POST.get('bon_tour_details')
        bon_want_register = request.POST.get('bon_want_register') 

        user = None
        # If user is logged in, use the existing user
        if request.user.is_authenticated:
            user = request.user
        # User create
        elif  bon_want_register: 
            parts = bon_name.rsplit(' ', 1)
            if len(parts) == 2:
                first_name = parts[0]  
                last_name = parts[1]    
            else:
                first_name = bon_name
                last_name = ''
            
            username = generate_unique_username(first_name, last_name)
            user = User.objects.create_user(
                        username=username,
                        first_name=first_name,
                        last_name=last_name,
                        email=bon_email,
                        password='123456'
                    )
            user.is_staff = True
            user.save()
        
         # Genrate Travel Enquiry
        TravelEnquiry.objects.create(
            user=user,
            name=bon_name,
            email=bon_email,
            phone_no=bon_phone,
            departure_date=bon_departure_date, 
            category_id=bon_category, 
            destination=bon_destination,
            country_id=bon_country, 
            duration=bon_duration, 
            no_person=bon_no_person,
            hotel_type = bon_hotel_type,
            tourdetails = bon_tour_details
        )
            
        messages.success(request, "Get a quick reply within 24 hours.")
        if request.user.is_authenticated:
            return redirect('travelEnquiry')
        else:
            return redirect('thankYouPage')
    
    tour_list = Categories.objects.filter(is_active=True).order_by('-id')
    country_list= Countries.objects.filter(is_active=True).order_by('country_name')
    package = None
    breadcrumb_title = 'Online Booking Enquiry'
    action_url = "" 
    if package_id:
        package = TravelPackage.objects.get(id=package_id)
        breadcrumb_title = 'Online Package Booking'
        action_url =  reverse('packageConfirmation')
        
    return render(request, 'pages/booking.html',{'title': 'Booking','breadcrumb_title': breadcrumb_title,'tour_list':tour_list,'country_list':country_list,'package_id':package_id,'package':package,'action_url':action_url})

def destination(request,country_id=None):
    country_list= Countries.objects.filter(is_active=True).order_by('country_name')
    
    if country_id:
        our_gallery = OurGallery.objects.filter(country_id=country_id).select_related('country').order_by('-created_at')
    else:
        our_gallery = OurGallery.objects.filter(is_active=True).select_related('country').order_by('-created_at')

    grouped_by_country = defaultdict(lambda: {
        'count': 0,
        'latest_image': None,
        'images': [],
    })
    for img in our_gallery:
        country = img.country.name if hasattr(img.country, 'name') else img.country  # handle FK or CharField
        grouped_by_country[country]['images'].append(img)
        grouped_by_country[country]['count'] += 1
        if grouped_by_country[country]['latest_image'] is None:
            grouped_by_country[country]['latest_image'] = img 
    return render(request, 'pages/destination.html',{'title': 'Destination','breadcrumb_title': 'Travel Destination','country_list':country_list,'grouped_by_country':dict(grouped_by_country),'country_id':country_id})

def exploreTour(request):
    tour_list = Categories.objects.filter(is_active=True).order_by('category_name')
    return render(request, 'pages/explore_tour.html',{'title': 'Tour','breadcrumb_title': 'Tour Category','tour_list':tour_list})   

def travelGuides(request):
    guides_list = TravelGuide.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'pages/travel_guides.html',{'title': 'Guides','breadcrumb_title': 'Our Travel Guides','guides_list': guides_list})  

def gallery(request,category_id=None):
    categories_list = Categories.objects.filter(is_active=True).order_by('category_name')
    our_gallery = OurGallery.objects.filter(is_active=True).order_by('-created_at')
    categories_info = None
    if category_id :
        categories_info = Categories.objects.filter(id=category_id).first()
        our_gallery = OurGallery.objects.filter(category_id=category_id).order_by('-created_at')
    
    return render(request, 'pages/gallery.html',{'title': 'Gallery','breadcrumb_title': 'Photo Gallery','our_gallery':our_gallery,'categories_list':categories_list,'category_id':category_id,'categories_info':categories_info})   

def careers(request):
    jobs = Jobs.objects.filter(is_active=True).order_by('-created_at')[:12]
    total = jobs.count()
    half = (total + 1) // 2 
    left_jobs = jobs[:half]
    right_jobs = jobs[half:]
    return render(request, 'pages/careers.html',{'title': 'Careers','breadcrumb_title': 'Careers','left_jobs':left_jobs,'right_jobs':right_jobs})   

def cmsContent(request, slug): 
    try:
        content = CMS.objects.get(slug=slug)
        return render(request, 'pages/cms_content.html', {'content': content, 'title': content.title, 'breadcrumb_title': content.title})
    except CMS.DoesNotExist:
        # If the CMS content does not exist, redirect to a 404 page or handle it accordingly
        return render(request, 'pages/404.html', status=404)
    
def blogDetails(request, slug):
    try:
        socialMediaLink = SocialMediaLink.objects.filter(is_active=True)
        blogs = Blog.objects.filter(is_active=True).exclude(slug=slug).order_by('-created_at')[:4]
        blog = Blog.objects.get(slug=slug)
        blogComments = blog.comments.filter(is_active=True).order_by('-created_at')
        commentCount = blogComments.count()
        errormessage = None
        if request.method == 'POST':
            name = request.POST.get('name')
            email = request.POST.get('email')
            comment = request.POST.get('comment')
            if not name or not email or not comment:
                messages.error(request, "All Filde requred!")
            else:
                new_comment = BlogComment(blog=blog, name=name, email=email, comment=comment)
                new_comment.save()
                messages.success(request, "Commetns has benn successfully submited!")
                return redirect('blogDetails', slug=slug)
        return render(request, 'pages/blog_details.html', {'blog': blog,'blogs': blogs, 'title': blog.title, 'breadcrumb_title': blog.title,'socialMediaLink': socialMediaLink,'blogComments': blogComments,'commentCount': commentCount})   
    except Blog.DoesNotExist:
        # If the blog post does not exist, redirect to a 404 page or handle it accordingly
        return render(request, 'pages/404.html', status=404)
    
def careersDetails(request, id):
    try:
        socialMediaLink = SocialMediaLink.objects.filter(is_active=True)
        jobInfo = Jobs.objects.get(id=id)
        otherJobs = Jobs.objects.filter(is_active=True).exclude(id=id)[:4]
        return render(request, 'pages/job_details.html', {'jobInfo': jobInfo,'socialMediaLink': socialMediaLink, 'title': jobInfo.title, 'breadcrumb_title': jobInfo.title,'otherJobs':otherJobs})   
    except Jobs.DoesNotExist:
        # If the blog post does not exist, redirect to a 404 page or handle it accordingly
        return render(request, 'pages/404.html', status=404)
    
def applyJob(request, id):
    try:
        socialMediaLink = SocialMediaLink.objects.filter(is_active=True)
        jobInfo = Jobs.objects.get(id=id)
        if request.method == 'POST':
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone_no')
            resume = request.FILES.get('resume')
            content = request.POST.get('content')
            if not name or not email or not phone or not resume:
                messages.error(request, "All fields are required!")
            else:
                new_application = ReceiveJobApplication(job=jobInfo, name=name, email=email, phone=phone, resume=resume,content = content)
                new_application.save()
                messages.success(request, "Your application has been successfully submitted!")
                return redirect('careersDetails', id=id)
        return render(request, 'pages/job_details.html', {'jobInfo': jobInfo, 'title': jobInfo.title, 'breadcrumb_title': jobInfo.title,'socialMediaLink': socialMediaLink})   
    except Jobs.DoesNotExist:
        # If the job does not exist, redirect to a 404 page or handle it accordingly
        return render(request, 'pages/404.html', status=404)   
    
def travelGuidesInfo(request, id): 
    try:
        socialMediaLink = SocialMediaLink.objects.filter(is_active=True)
        otherGuide = TravelGuide.objects.filter(is_active=True).exclude(id=id).order_by('-created_at')[:4]
        guideInfo = TravelGuide.objects.get(id=id)
        return render(request, 'pages/guides_details.html', {'guideInfo': guideInfo,'otherGuide': otherGuide,'socialMediaLink': socialMediaLink, 'title': guideInfo.name, 'breadcrumb_title': guideInfo.name})
    except CMS.DoesNotExist:
        # If the CMS content does not exist, redirect to a 404 page or handle it accordingly
        return render(request, 'pages/404.html', status=404)

def servicesDetails(request, id):
    try:
        socialMediaLink = SocialMediaLink.objects.filter(is_active=True)
        ourServicesInfo = OurServices.objects.get(id=id)
        otherServices = OurServices.objects.filter(is_active=True).exclude(id=id).order_by('-created_at')[:4]
        return render(request, 'pages/services_details.html', {'ourServicesInfo': ourServicesInfo,'socialMediaLink': socialMediaLink, 'title': ourServicesInfo.title, 'breadcrumb_title': ourServicesInfo.title,'otherServices':otherServices})   
    except Jobs.DoesNotExist:
        # If the blog post does not exist, redirect to a 404 page or handle it accordingly
        return render(request, 'pages/404.html', status=404)
    
def userSendEnquiry(request): 
    if request.method == 'POST':
        name = request.POST.get('user_name')
        email = request.POST.get('user_email')
        subject = request.POST.get('user_subject')
        message = request.POST.get('user_message')
        
        if not name or not email or not subject or not message:
            messages.error(request, "All fields are required!")
        else:
            UserEnquiry.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message
            )
            messages.success(request, "Your enquiry has been successfully submitted!")
        return redirect('contact')  # Redirect to contact page
    return redirect('contact')  # If not POST, redirect as well
    
def subscribe(request): 
    if request.method == 'POST':
        email = request.POST.get('subscribe_email')
        
        if not email:
            return JsonResponse({"error": "Invalid Email ID"}, status=400)

        if Subscribers.objects.filter(email=email).exists():
            return JsonResponse({"error": "This email is already subscribed."}, status=409)

        Subscribers.objects.create(email=email)
        return JsonResponse({"message": "Subscribed successfully"}, status=200)

    return JsonResponse({"error": "Invalid request method"}, status=405)

def packagesInfo(request, slug): 
    try:
        socialMediaLink = SocialMediaLink.objects.filter(is_active=True)
        otherPackage = TravelPackage.objects.filter(is_active=True).exclude(slug=slug).order_by('-created_at')[:4]
        packageInfo = TravelPackage.objects.get(slug=slug)
        return render(request, 'pages/packages_details.html', {'packageInfo': packageInfo,'otherPackage': otherPackage,'socialMediaLink': socialMediaLink, 'title': packageInfo.package_name, 'breadcrumb_title': packageInfo.package_name})
    except CMS.DoesNotExist:
        # If the CMS content does not exist, redirect to a 404 page or handle it accordingly
        return render(request, 'pages/404.html', status=404)


def thankYouPage(request): 
    return render(request, 'pages/thank_you.html', {'title': 'Thank You', 'breadcrumb_title': 'Thank You'})

def registrationsPage(request): 
    return render(request, 'pages/auth/registrationsPage.html', {'title': 'Registration', 'breadcrumb_title': 'Registration'})

def registrations(request):
    try:
        if request.method == 'POST':
            userForm = CreateUserForm(request.POST)
            if userForm.is_valid():
                user = userForm.save(commit=False)
                user.is_staff = True
                user.save()
                username = userForm.cleaned_data.get('username')
                messages.success(request, 'Thank you for registration ' + username)
                return redirect('thankYouPage')
            else:
                messages.error(request, "Please correct the errors below.")
        else:
            userForm = CreateUserForm()

        return render(request, 'pages/auth/registrationsPage.html', {
            'form': userForm,
            'title': 'Registration',
            'breadcrumb_title': 'Registration'
        })

    except Exception as e:
        print("Error during registration:", e)
        return render(request, 'pages/404.html', status=404)


# User dashboard
@login_required(login_url='loginPage')
def dashboard(request): 
    booking_stats = BookingList.objects.filter(user=request.user).aggregate(
        total_bookings=Count('id'),
        total_amount=Sum('total_amount')
    )
    total_booking = booking_stats['total_bookings']
    total_booking_amount = booking_stats['total_amount'] or 0
    # total_booking = BookingList.objects.filter(user=request.user).count()
    total_enquiry = TravelEnquiry.objects.filter(user=request.user).exclude(id__in=BookingList.objects.values_list('TravelEnquiry_id', flat=True)).count()
    return render(request, 'pages/userInfo/dashboard.html', {'title': 'Dashboard', 'breadcrumb_title': 'Dashboard','total_booking':total_booking,'total_enquiry':total_enquiry,'total_booking_amount':total_booking_amount})

# User Booking List
@login_required(login_url='loginPage')
def bookingList(request): 
    booking_list = BookingList.objects.filter(user=request.user).order_by('-id')
    return render(request, 'pages/userInfo/booking_list.html', {'title': 'Booking List', 'breadcrumb_title': 'Booking List','booking_list':booking_list})

# User Travel Enquiry
@login_required(login_url='loginPage')
def travelEnquiry(request): 
    user = request.user
    travel_enquiry_list = TravelEnquiry.objects.filter(user=user).exclude(id__in=BookingList.objects.values_list('TravelEnquiry_id', flat=True))
    return render(request, 'pages/userInfo/travel_enquiry.html', {'title': 'Travel Enquiry', 'breadcrumb_title': 'Travel Enquiry','travel_enquiry_list':travel_enquiry_list})

# User profile
@login_required(login_url='loginPage')
def userProfile(request): 
    user = request.user
    u_profile, created = UserProfile.objects.get_or_create(user=user) 
    if request.method == 'POST':
        # user fields
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')

        # profile fields
        u_profile.phone = request.POST.get('phone')
        u_profile.country_id = request.POST.get('country')
        u_profile.address = request.POST.get('address')
        if request.FILES.get('profile_image'):
            u_profile.profile_image = request.FILES.get('profile_image')

        user.save()
        u_profile.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('userProfile')
    # country list
    country_list= Countries.objects.filter(is_active=True).order_by('country_name')
    return render(request, 'pages/userInfo/user_profile.html', {'title': 'User Profile', 'breadcrumb_title': 'User Profile','country_list':country_list,'u_profile':u_profile})

# Change password
@login_required(login_url='loginPage')
def changePassword(request): 
    if request.method == 'POST':
        old_pass = request.POST.get('old_password')
        new_pass1 = request.POST.get('new_password1')
        new_pass2 = request.POST.get('new_password2')

        if not request.user.check_password(old_pass):
            messages.error(request, "Old password is incorrect.")
        elif new_pass1 != new_pass2:
            messages.error(request, "New passwords do not match.")
        else:
            try:
                validate_password(new_pass1, user=request.user)
                request.user.set_password(new_pass1)
                request.user.save()
                update_session_auth_hash(request, request.user)  # keeps session active
                messages.success(request, "Password changed successfully.")
                return redirect('changePassword')  # or wherever you want to go after change
            except Exception as e:
                messages.error(request, f"Error: {e}")
    return render(request, 'pages/userInfo/change_password.html', {'title': 'Change Password', 'breadcrumb_title': 'Change Password'})

# User Gallery
@login_required(login_url='loginPage')
def userGallery(request): 
    if request.method == 'POST':
        img_title = request.POST.get('img_title')
        img_category = request.POST.get('img_category')
        img_country = request.POST.get('img_country')
        thumbnail_image = request.FILES.get('thumbnail_image') 
        OurGallery.objects.create(
            title=img_title,
            category_id=img_category,
            country_id=img_country,
            thumbnail_image=thumbnail_image,
            user=request.user  # Assign the current user
        )
        messages.success(request, "Image uploaded successfully.")
        return redirect('userGallery')
    
    # User Image
    user_images_list = OurGallery.objects.filter(user=request.user).order_by('-id')
    # Category
    categories_list = Categories.objects.filter(is_active=True).order_by('category_name')
    # country list
    country_list= Countries.objects.filter(is_active=True).order_by('country_name')
    return render(request, 'pages/userInfo/user_gallery.html', {'title': 'User Gallery', 'breadcrumb_title': 'User Gallery','country_list':country_list,'categories_list':categories_list,'user_images_list':user_images_list})

# delete User Image
@login_required(login_url='loginPage')
def deleteUserImage(request, id):
    try:
        image = get_object_or_404(OurGallery, id=id, user=request.user)
        image.delete()
        messages.success(request, "Image deleted successfully.")
    except:
        messages.error(request, "Image could not be deleted or was not found.")

    return redirect('userGallery')

# delete User enquiry
@login_required(login_url='loginPage')
def deleteUserEnquiry(request, id):
    try:
        enquiry = get_object_or_404(TravelEnquiry, id=id, user=request.user)
        enquiry.delete()
        messages.success(request, "Enquiry deleted successfully.")
    except:
        messages.error(request, "Enquiry could not be deleted or was not found.")

    return redirect('travelEnquiry')

# get travel enquiry 
@login_required(login_url='loginPage')
def getTravelEnquiry(request):
    enquiry_id = request.GET.get('id')
    try:
        enquiry = TravelEnquiry.objects.get(id=enquiry_id)
        day_label = "Day" if enquiry.duration == 1 else "Days"
        duration = f"{enquiry.duration} {day_label}"
        data = {
            'name': enquiry.name,
            'email': enquiry.email,
            'phone_no': enquiry.phone_no,
            'created_date': enquiry.created_at.strftime('%Y-%m-%d'),
            'departure_date': enquiry.departure_date.strftime('%Y-%m-%d'),
            'destination': enquiry.destination,
            'duration': duration,
            'country': enquiry.country.country_name,
            'hotel_type': enquiry.get_hotel_type_display(),
            'no_person': enquiry.no_person,
            'category': enquiry.category.category_name,
            'tourdetails': enquiry.tourdetails,
        }
        return JsonResponse(data)
    except TravelEnquiry.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)
    
# get Quotation 
@login_required(login_url='loginPage')
def getQuotation(request):
    enquiry_id = request.GET.get('id')
    try:
        quotationInfo = QuotationInfo.objects.get(travelEnquiry_id=enquiry_id) 
        data = {
            'price': quotationInfo.quotation_amount,
            'deacription': quotationInfo.quotation_deacription, 
        }
        return JsonResponse(data)
    except TravelEnquiry.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)

# Login Page
def loginPage(request): 
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request, 'Username or password invalid')  
            return render(request, 'pages/auth/loginPage.html', {
                'title': 'Login',
                'breadcrumb_title': 'Login'
            })

    return render(request, 'pages/auth/loginPage.html', {
        'title': 'Login',
        'breadcrumb_title': 'Login'
    })

# Booking Confirmation
def bookingConfirmation(request,id):
    tax_list = TaxSetting.objects.filter(is_active=True).order_by('id')
    enquiry = TravelEnquiry.objects.get(id=id)
    quotationInfo = QuotationInfo.objects.get(travelEnquiry_id=id)
    day_label = "Day" if enquiry.duration == 1 else "Days"
    duration = f"{enquiry.duration} {day_label}"
    departure_date = enquiry.departure_date.strftime('%d/%m/%Y')
    hotel_type_display = enquiry.get_hotel_type_display()

    sub_total = float(quotationInfo.quotation_amount)
    total_tax = 0
    for tax in tax_list:
        if tax.text_apply_type == 'Flat':
            total_tax += float(tax.tax_value)
        else:
            # Apply percentage tax
            percent_tax = (float(tax.tax_value) / 100) * sub_total
            total_tax += percent_tax

    grand_total = sub_total + total_tax

    tax_list_new = list(tax_list.values())
    tax_list_json = json.dumps(tax_list_new, cls=DjangoJSONEncoder)
    
    return render(request, 'pages/bookingConfirmation.html', {
        'title': 'Booking Confirmation',
        'breadcrumb_title': 'Booking Confirmation','enquiry':enquiry,'duration':duration,'departure_date':departure_date,'hotel_type_display':hotel_type_display,'quotationInfo':quotationInfo,'tax_list':tax_list,'all_tax_info':tax_list_json,'grand_total':grand_total,'total_tax':total_tax
    })

# payment process Now
@csrf_exempt
def payNow(request):
    if request.method == 'POST':
        order_id = random.randint(10000000, 99999999)
        data = request.POST
        # Amount and other details
        booking_type = data.get('booking_type')
        sub_total_amount = data.get('sub_total_amount')
        total_tax_amount = data.get('total_tax_amount')
        total_amount = data.get('total_amount')
        tax_details = data.get('tax_details')
        # Basic user Info
        inserted_id = ""
        name  = ""
        email = ""
        phone_no = ""
        # Travling Info
        departure_date = ""
        category = ""
        destination = ""
        country = ""
        duration = ""
        no_person = ""
        hotel_type = ""
        tourdetails = ""
        new_order_id = ""
        # ALL travel enquiry info
        travel_enquiry = None
        # All QuotationI nfo
        quotation = None
        # package Info
        package = None
        # Common ID
        common_id = ""
        if booking_type == 'Quotation':
            enquiry_id = data.get('enquiry_id')
            new_order_id = str(order_id) + str(enquiry_id)
            travel_enquiry = TravelEnquiry.objects.get(id=enquiry_id)
            # Get User Information
            user = User.objects.get(id=travel_enquiry.user_id)
            # Get Quotation Information
            quotation = QuotationInfo.objects.get(travelEnquiry_id=enquiry_id)
            # Booking Data
            name = travel_enquiry.name
            email = travel_enquiry.email  
            phone_no = travel_enquiry.phone_no  
            departure_date = travel_enquiry.departure_date
            category = travel_enquiry.category
            destination = travel_enquiry.destination
            country = travel_enquiry.country
            duration = travel_enquiry.duration
            no_person = travel_enquiry.no_person
            hotel_type = travel_enquiry.hotel_type
            tourdetails = travel_enquiry.tourdetails 
            user_id = travel_enquiry.user_id   
            common_id = enquiry_id
            
        else:
            bon_package_id = request.POST.get("userData[bon_package_id]")
            new_order_id = str(order_id) + str(bon_package_id)
            bon_name = request.POST.get("userData[bon_name]")
            bon_email = request.POST.get("userData[bon_email]")
            bon_phone = request.POST.get("userData[bon_phone]")
            bon_departure_date = request.POST.get("userData[bon_departure_date]")
            bon_tour_details = request.POST.get("userData[bon_tour_details]")
            bon_want_register = request.POST.get("userData[bon_want_register]")
            user = None
            if request.user.is_authenticated:
                user = request.user
            elif  bon_want_register: 
                parts = bon_name.rsplit(' ', 1)
                if len(parts) == 2:
                    first_name = parts[0]  
                    last_name = parts[1]    
                else:
                    first_name = bon_name
                    last_name = ''
                
                username = generate_unique_username(first_name, last_name)
                user = User.objects.create_user(
                            username=username,
                            first_name=first_name,
                            last_name=last_name,
                            email=bon_email,
                            password='123456'
                        )
                user.is_staff = True
                user.save()
            
            name = bon_name
            email = bon_email 
            phone_no = bon_phone 
            departure_date = bon_departure_date
            tourdetails = bon_tour_details
            # Get Travel Package Info
            package = TravelPackage.objects.get(id=bon_package_id)
            category = package.category
            destination = package.destination
            country = package.country
            duration = package.duration
            no_person = package.no_person
            hotel_type = package.hotel_type
            common_id = bon_package_id
            
        
        # Save Booking Data
        bookingData = BookingList.objects.create(
                booking_type=booking_type,
                TravelEnquiry=travel_enquiry, 
                quotationInfo=quotation, 
                travelPackage=package, 
                user=user,
                name=name,
                email=email,
                phone_no=phone_no,
                departure_date=departure_date,
                category=category,
                destination=destination,
                country=country,
                duration=duration,
                no_person=no_person,
                hotel_type=hotel_type,
                tourdetails=tourdetails,
                
                # Billing info
                order_id=new_order_id, 
                total_amount=total_amount,
                sub_total_amount=sub_total_amount,
                other_charges_amount=total_tax_amount,
                other_charges_info=tax_details,
                payment_status="pending",
                # Optional (these are auto-set)
                is_active=True
            )
        # current Insert ID 
        inserted_id = bookingData.id
            
        # Get Razorpay Setting
        razorpaySetting = RazorpaySetting.objects.first()
        payment_id = str(order_id)+str(common_id)+str(inserted_id)
        amount_paise = int(float(total_amount) * 100)
        client = razorpay.Client(auth=(razorpaySetting.razorpay_key_id, razorpaySetting.razorpay_secret_key))
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
                'booking_type': booking_type,
                'payment_id': razorpay_order['id'],
                'razorpay_key_id': razorpaySetting.razorpay_key_id,
                'amount': total_amount,
                'success_url': '/razorpay-success',
                'booking_id': bookingData.id,
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
            bookingData = BookingList.objects.get(id=booking_id)
            bookingData.payment_status = 'success'
            bookingData.save()
            return JsonResponse({
                "redirect_url": "/bookingReceipt/" + str(booking_id),
                "message": "Payment successful and booking confirmed."
            })
        except BookingList.DoesNotExist:
            return JsonResponse({"error": "Booking not found."}, status=404)

    except Exception as e:
        print("Error in razorpaySuccess:", e)
        return JsonResponse({"error": str(e)}, status=500)
    
# Booking Receipt
@csrf_exempt 
def bookingReceipt(request, id):
    bookingData = BookingList.objects.get(id=id)
    departure_date = bookingData.departure_date.strftime('%d/%m/%Y')
    return render(request, 'pages/bookingReceipt.html', {
        'title': 'Booking Receipt',
        'breadcrumb_title': 'Booking Receipt',
        'bookingID': id,
        'bookingData': bookingData,
        'hotel_type_display': bookingData.get_hotel_type_display(),
        'departure_date': departure_date,
    })

def downloadReceiptPDF(request,id):
    siteData = Setting.objects.first()
    bookingData = BookingList.objects.get(id=id)
    hotel_type_display = bookingData.get_hotel_type_display()
    context = {
        "siteData": siteData,
        "bookingData": bookingData,
        "hotel_type_display": hotel_type_display,
        'departure_date': bookingData.departure_date.strftime('%Y-%m-%d'),
    }
    html = render_to_string("pages/receipt_pdf.html", context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="receipt.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("Error creating PDF", status=500)

    return response

def packageConfirmation(request):
    if request.method == 'POST':
        tax_list = TaxSetting.objects.filter(is_active=True).order_by('id')
        # Example: fetch form data
        bon_name = request.POST.get("bon_name")
        bon_email = request.POST.get("bon_email")
        bon_phone = request.POST.get("bon_phone")
        bon_departure_date = request.POST.get("bon_departure_date") 
        bon_tour_details = request.POST.get("bon_tour_details") 
        bon_package_id = request.POST.get("bon_package_id") 
        bon_want_register = request.POST.get('bon_want_register') 
        package = TravelPackage.objects.get(id=bon_package_id)
        
        day_label = "Day" if package.duration == 1 else "Days"
        duration = f"{package.duration} {day_label}"

        package_amount = package.offer_price if package.offer_price else package.price
        sub_total = float(package_amount)
        total_tax = 0
        for tax in tax_list:
            if tax.text_apply_type == 'Flat':
                total_tax += float(tax.tax_value)
            else:
                # Apply percentage tax
                percent_tax = (float(tax.tax_value) / 100) * sub_total
                total_tax += percent_tax

        grand_total = sub_total + total_tax

        tax_list_new = list(tax_list.values())
        tax_list_json = json.dumps(tax_list_new, cls=DjangoJSONEncoder)


        return render(request, "pages/package_confirmation.html", {
            'title': 'Package Confirmation',
            'breadcrumb_title': 'Package Confirmation',
            "bon_name": bon_name,
            "bon_email": bon_email,
            "bon_phone": bon_phone,
            "bon_departure_date":  bon_departure_date,
            "bon_tour_details": bon_tour_details,
            "bon_package_id": bon_package_id,
            "package": package,
            "duration": duration,
            "bon_want_register": bon_want_register,
            "hotel_type_display":package.get_hotel_type_display(),
            "sub_total": sub_total,
            "total_tax": total_tax,
            "grand_total": grand_total, 
            "all_tax_info":tax_list_json,
            "tax_list": tax_list,
        })
    else:
        return redirect('packages')
    
# logout User
def logoutUser(request):
    logout(request)
    return redirect('loginPage')
