"""
URL configuration for dj_19 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from dj_19 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('booking-list/', views.bookingList, name='bookingList'),
    path('get-travel-enquiry/', views.getTravelEnquiry, name='getTravelEnquiry'),
    path('travel-enquiry/', views.travelEnquiry, name='travelEnquiry'),
    path('get-quotation/', views.getQuotation, name='getQuotation'),
    path('delete-travel-enquiry/<int:id>/', views.deleteUserEnquiry, name='deleteUserEnquiry'),
    path('user-profile/', views.userProfile, name='userProfile'),
    path('change-password/', views.changePassword, name='changePassword'),
    path('user-gallery/', views.userGallery, name='userGallery'),
    path('delete-user-image/<int:id>/', views.deleteUserImage, name='deleteUserImage'),
    path('user-signup/', views.registrationsPage, name='registrationsPage'),
    path('registrations/', views.registrations, name='registrations'),
    path('thank-you/', views.thankYouPage, name='thankYouPage'),
    path('login/', views.loginPage, name='loginPage'),
    path('logout/', views.logoutUser, name='logout'),
    path('about/', views.about, name='about'),
    path('package-confirmation/', views.packageConfirmation, name='packageConfirmation'),
    path('booking-confirmation/<int:id>/', views.bookingConfirmation, name='bookingConfirmation'),
    path('razorpay-success',views.razorpaySuccess,name='razorpaySuccess'),
    path('bookingReceipt/<int:id>/', views.bookingReceipt, name='bookingReceipt'),
    path('download-receipt/<int:id>/',views.downloadReceiptPDF,name='downloadReceiptPDF'),
    path('pay-now/', views.payNow, name='payNow'),
    path('services/', views.services, name='services'),
    path('services/<int:id>/', views.servicesDetails, name='servicesDetails'),
    path('packages/', views.packages, name='packages_list'),
    path('packages/<int:category_id>/', views.packages, name='packages'),
    path('packages/<slug:slug>/', views.packagesInfo, name='packagesInfo'),
    path('blog/', views.blog, name='blog'),
    path('blog/<slug:slug>/', views.blogDetails, name='blogDetails'),
    path('contact/', views.contact, name='contact'),
    path('send-enquiry/', views.userSendEnquiry, name='userSendEnquiry'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('booking/', views.booking, name='booking'),
    path('booking/<int:package_id>/', views.booking, name='booking_with_id'),
    path('destination/', views.destination, name='destination'),
    path('destination/<int:country_id>/', views.destination, name='destination_country_id'),
    path('explore-tour/', views.exploreTour, name='exploreTour'),
    path('travel-guides/', views.travelGuides, name='travelGuides'),
    path('guide/<int:id>/', views.travelGuidesInfo, name='travelGuidesInfo'),
    path('gallery/', views.gallery, name='gallery'),
    path('gallery/<int:category_id>/', views.gallery, name='gallery_category_id'),
    path('careers/', views.careers, name='careers'),
    path('careers/<int:id>/', views.careersDetails, name='careersDetails'),
    path('apply-job/<int:id>/', views.applyJob, name='applyJob'),
    path('<slug:slug>/', views.cmsContent, name='cmsContent'),
    path('api/',include('api.urls')),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)