from django.shortcuts import render
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework.response import Response

# serializers
from api.serializers.site_serializers import SiteSettingSerializers , SocialMediaLinkSerializer , AboutUsSerializer ,SliderListSerializer,GalleryListSerializer,CategoryListSerializer,CountryListSerializer,CMSSerializer,TestimonialSerializer,ServicesSerializer,TravelGuidesSerializer

from api.serializers.careers_serializers import jobsSerializer,ApplyJobSerializer

# Model
from setting.models import Setting,SocialMediaLink,AboutUs,Slider, OurGallery , Categories , Countries 
from cms.models import CMS
from travelGuides.models import Testimonial,OurServices,TravelGuide
from jobs.models import Jobs,ReceiveJobApplication

# responce site info , all social media link , about us
@api_view()
def get_site_info(request):
    # Site Inforamtion
    siteQuerySet = Setting.objects.first()
    siteSerializer = SiteSettingSerializers(siteQuerySet) if siteQuerySet else None
    # Site social links  
    SocialMediaLinkQuerySet = SocialMediaLink.objects.filter(is_active=True)
    siteSocialMediaLinkSerializer = SocialMediaLinkSerializer(SocialMediaLinkQuerySet,many=True)
    # About US
    AboutUsQuerySet = AboutUs.objects.first()
    siteAboutUsSerializer = AboutUsSerializer(AboutUsQuerySet) if AboutUsQuerySet else None
    
    return Response({
    'site_info_data': siteSerializer.data if siteSerializer else None,
    'social_media_link': siteSocialMediaLinkSerializer.data,
    'about_us': siteAboutUsSerializer.data if siteAboutUsSerializer else None
    }) 

# Slider List and Gallery
@api_view()
def slider_and_gallery(request):
    # Slider List
    sliderListSet  =Slider.objects.filter(is_active=True)
    set_SliderListSerializer = SliderListSerializer(sliderListSet,many=True)
    # Gallery List
    galleryList_set = OurGallery.objects.filter(is_active=True)
    set_galleryList = GalleryListSerializer(galleryList_set,many=True)

    return Response({
        'slider_list':set_SliderListSerializer.data,
        'gallery_list':set_galleryList.data
    })

# Category List and Country
@api_view()
def category_and_country(request):
    # Category List
    categoryList_set = Categories.objects.filter(is_active=True)
    set_categoryList = CategoryListSerializer(categoryList_set,many=True)
    # Countries List
    countries_set = Countries.objects.filter(is_active=True)
    set_countries = CountryListSerializer(countries_set,many=True)

    return Response({
        'categories_list':set_categoryList.data,
        'countries_list':set_countries.data,
    })

# page content
@api_view()
def page_content(request,slug):
    pageContent_set = CMS.objects.filter(slug=slug)
    set_pageContent = CMSSerializer(pageContent_set,many=True)
    return Response({
        'pageContent':set_pageContent.data, 
    })

# Testimonial
@api_view()
def get_testimonial(request):
    testimonial_set = Testimonial.objects.filter(is_active=True)
    set_testimonial = TestimonialSerializer(testimonial_set,many=True)
    return Response({
        'testimonial_list':set_testimonial.data, 
    })

# services
@api_view()
def get_services(request):
    ourServices_set = OurServices.objects.filter(is_active=True).order_by('-created_at')
    set_ourServices = ServicesSerializer(ourServices_set,many=True)
    return Response({
        'services_list':set_ourServices.data, 
    })

# services Details
@api_view()
def services_detail(request,id):
    ourServicesDetails_set = OurServices.objects.filter(id=id).order_by('-created_at')
    set_ourServicesDetails = ServicesSerializer(ourServicesDetails_set,many=True)
    return Response({
        'services_details':set_ourServicesDetails.data, 
    })

# Travel Guides
@api_view()
def travel_guides(request):
    travelGuide_set = TravelGuide.objects.filter(is_active=True).order_by('-created_at')
    set_travelGuide = TravelGuidesSerializer(travelGuide_set,many=True)
    return Response({
        'travel_guide_list':set_travelGuide.data, 
    })

# guides Details
@api_view()
def guides_detail(request,id):
    travelGuideDetails_set = TravelGuide.objects.filter(id=id).order_by('-created_at')
    set_travelGuideDetails = TravelGuidesSerializer(travelGuideDetails_set,many=True)
    return Response({
        'services_details':set_travelGuideDetails.data, 
    })

# Jobs
@api_view()
def job_list(request):
    job_list_set = Jobs.objects.filter(is_active=True).order_by('-created_at')
    set_job_list = jobsSerializer(job_list_set,many=True)
    return Response({
        'job_list':set_job_list.data, 
    })

# Jobs Details
@api_view()
def job_details(request,id):
    job_details_set = Jobs.objects.filter(id=id)
    set_job_details = jobsSerializer(job_details_set,many=True)
    return Response({
        'job_details':set_job_details.data, 
    })

# apply job
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def apply_job(request):
    job_id = request.POST.get('job_id')
    try:
        jobInfo = Jobs.objects.get(id=job_id)
    except Jobs.DoesNotExist:
        return Response({"error": "Invalid job_id"}, status=status.HTTP_400_BAD_REQUEST)

    name = request.POST.get('name')
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    content = request.POST.get('content')
    resume = request.FILES.get('resume')

    # Required fields validation
    if not name or not email or not phone or not resume:
        return Response(
            {"error": "Name, Email, Phone, and Resume are required."},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    data = {
        "job": job_id,    
        "name": name,
        "email": email,
        "phone": phone,
        "content": content,
        "resume": resume
    }

    apply_job_set = ApplyJobSerializer(data=data)

    if apply_job_set.is_valid():
        apply_job_set.save()
        return Response({"message": "Application submitted successfully"}, status=status.HTTP_201_CREATED)

    return Response(apply_job_set.errors, status=status.HTTP_400_BAD_REQUEST)


# Booking Enquiry
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def booking_enquiry(request):
    user_id = request.POST.get('user_id')
    name = request.POST.get('name')
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    content = request.POST.get('content')
    departure_date = request.POST.get('departure_date')
    no_person = request.POST.get('no_person')
    hotel_type = request.POST.get('hotel_type')
    category = request.POST.get('category')
    country = request.POST.get('country')
    destination = request.POST.get('destination')
    duration = request.POST.get('duration')
    tour_details = request.POST.get('tour_details')
    want_register = request.POST.get('want_register')
    

    return Response(apply_job_set.errors, status=status.HTTP_400_BAD_REQUEST)
