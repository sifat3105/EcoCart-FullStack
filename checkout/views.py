from django.shortcuts import render, redirect
from cart.views import get_cart_data, ShoppigData
from urllib.parse import urlencode
from accounts.models import Customer

def checkout_view(request):
    if not request.user.is_authenticated:
        return redirect('authentication')
    customer, created = Customer.objects.get_or_create(user=request.user)
    shipping = ShoppigData.objects.get(user=request.user)
    context = get_cart_data(request)
    context['full_name'] = f"{request.user.first_name} {request.user.last_name}"
    context['email'] = request.user.email
    context['number'] = shipping.number
    context['shipping'] = f"{shipping.address}, {shipping.upazila}, {shipping.district}, {shipping.division}"
    shipping_fee= context['shipping_fee']
    if request.method == 'POST':
        data = request.POST.dict()
        shipping_address = data.get('shipping_address')
        if ',' in shipping_address:
            address_parts = [part.strip() for part in shipping_address.split(',')]
        else:
            address_parts = [part.strip() for part in shipping_address.split(' ')]
        
 
        new_entry = ShoppigData.objects.update(
            user = request.user,
            full_name = data.get('billing_name'),
            division = address_parts[-1],
            district = address_parts[-2],
            upazila = address_parts[-3],
            address = ', '.join(address_parts[:-3]),
            number = data.get('billing_phone'),
        )
        payment_method = request.POST.get('payment_method')

        data = {
                'total_amount': context['total'],
                "customer_name": context['full_name'],
                "customer_email": context['email'],
                "Customer Address": shipping_address,
                "customer_phone": context['number'],
                "domain": context['domain'],
                "shipping_fee": shipping_fee,
            }
        
        if payment_method == 'cash_on_delivery':
            params = urlencode(data)
            redirect_url = f'http://{context['domain']}/payment/cash-on-delivery?{params}'
            return redirect(redirect_url)
        elif payment_method == 'sslcommerz':
            
            params = urlencode(data)
            redirect_url = f'http://{context['domain']}/payment/sslcommerz?{params}'
            return redirect(redirect_url)
        
    return render(request, 'checkout/checkout.html', context)



