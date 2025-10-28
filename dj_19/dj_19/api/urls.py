"""
URL configuration for dj_18 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from dj_19 import views
from api import views

urlpatterns = [
    # Site Info
    path('get-site-info/', views.get_site_info, name='get_site_info'),
    path('slider-and-gallery/', views.slider_and_gallery, name='slider_and_gallery'),
    path('category-and-country/', views.category_and_country, name='category_and_country'),
    path('page/<slug:slug>/', views.page_content, name='page_content'),
    path('testimonial/', views.get_testimonial, name='get_testimonial'),
    # services List
    path('services/', views.get_services, name='get_services'),
    path('services-detail/<int:id>', views.services_detail, name='services_detail'),
    # Travel Guides
    path('travel-guides/', views.travel_guides, name='travel_guides'),
    path('guides-detail/<int:id>', views.guides_detail, name='guides_detail'),
    # Careers
    path('jobs/', views.job_list, name='job_list'),
    path('jobs-detail/<int:id>', views.job_details, name='job_details'),
    path("apply-job/", views.apply_job, name="apply-job"),
    # Booking Enquiry
    path("booking-enquiry/", views.booking_enquiry, name="booking-enquiry"),
]
 