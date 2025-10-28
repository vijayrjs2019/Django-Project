# middleware.py
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

class BlockNonAdminMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_paths = [
            '/travel-enquiry',
            '/booking-list',
            '/user-gallery',
            '/user-profile',
            '/change-password',
            '/dashboard',
        ]

        # Block normal user from admin panel
        if request.user.is_authenticated:
            if request.path.startswith('/admin'):
                if not request.user.is_superuser:
                    return redirect(reverse('home'))  # or replace with '/home/' if no name

            # Block admin from user-only pages
            elif any(request.path.startswith(path) for path in user_paths):
                if request.user.is_superuser:
                    return redirect(reverse('home'))  # or replace with '/home/'

        return self.get_response(request)
