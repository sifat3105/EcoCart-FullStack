from django.shortcuts import render, redirect
from cart.views import get_cart_data, ShoppigData

def checkout_view(request):
    if not request.user.is_authenticated:
        return redirect('authentication')
    shipping = ShoppigData.objects.get(user=request.user)
    context = get_cart_data(request)
    context['full_name'] = f"{request.user.first_name} {request.user.last_name}"
    context['email'] = request.user.email
    context['number'] = request.user.user_profile.phone_number
    context['shipping'] = f"{shipping.address} {shipping.upazila} {shipping.district} {shipping.division}"
    print(request.user.shippig)
    print(context)
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        
        if payment_method == 'cash_on_delivery':
            # Handle Cash on Delivery logic
            pass
        elif payment_method == 'sslcommerz':
            # Redirect to SSLCommerz payment gateway
            # return redirect('sslcommerz_payment')
            pass
        
        # Save order and redirect to confirmation page
    return render(request, 'checkout/checkout.html', context)

