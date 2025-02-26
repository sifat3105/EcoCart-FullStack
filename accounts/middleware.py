from django.shortcuts import redirect
from django.urls import reverse
from django.core.exceptions import PermissionDenied

class SellerVerificationMiddleware:
    """
    Middleware to restrict access to sellers who are not verified or inactive.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the user is authenticated and is a seller
        if request.user.is_authenticated and hasattr(request.user, 'seller'):
            seller = request.user.seller
            restricted_paths = [reverse('seller_dashboard'), reverse('add_product')]
            
            if request.path in restricted_paths:
                if not seller.is_active:
                    return redirect('seller_activation_pending')
                if not seller.is_verified:
                    raise PermissionDenied("Your seller account is not verified yet.")

        response = self.get_response(request)
        return response