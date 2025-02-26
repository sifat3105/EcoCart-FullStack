from cart.views import Cart
from django.urls import reverse
from django.shortcuts import render, get_object_or_404



def global_variables(request):
    account = "Login/Register"
    account_link = reverse("authentication")
    current_url = request.resolver_match.url_name
    print(current_url)
    search_history = request.session.get('search_history', [])
    cart = None

    if request.user.is_authenticated:
        account = request.user.username
        # account_link = reverse("account", kwargs={"username": account})   
        
        try:
            cart, created = Cart.objects.get_or_create(user=request.user)
        except Exception as e:
            cart = None

    return {
        "account": account,
        "account_link": account_link,
        "cart": cart if cart else None,
        "current_url":current_url,
        "search_history":search_history,
    }