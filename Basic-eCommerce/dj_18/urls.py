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
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from dj_18 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('about-us/',views.about,name='about'),
    path('furnitures/',views.furnitures,name='furnitures'),
    path('furnitures/<int:category_id>/', views.furnitures, name='furnitures_by_category'),
    path('furnitures/<slug:slug>/',views.furnituresDetail,name='furnituresDetail'),
    path('blog/',views.blog,name='blog'),
    path('blog/<slug:slug>/', views.blogDetail, name='blogDetail'),
    path('contact-us',views.contactUs,name='contactUs'), 
    path('subscribe',views.subscribe,name='subscribe'),
    path('checkout',views.checkOut,name='checkOut'),
    path('processToPayment',views.processToPayment,name='processToPayment'),
    path('cod-success',views.paymentSuccessCOD,name='paymentSuccessCOD'),
    path('payment-success',views.paymentSuccessGateway,name='paymentSuccessGateway'),
    path('razorpay-success',views.razorpay_success,name='razorpay_success'),
    path('api/',include('api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)