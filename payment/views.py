from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest
from sslcommerz_lib import SSLCOMMERZ
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from cart.views import get_cart_data
from accounts.models import Customer
from order.views import create_order
from urllib.parse import urlencode
from order.models import Order
from .models import Payment
import time, uuid, random

# Create your views here

def sslcommerz_payment(request):
    customer = Customer.objects.get(user = request.user)
    customer_id = customer.id
    # Form the transaction ID
    transaction_id = f"TNX-{str(uuid.uuid4())[:4]}-00{customer_id}-{str(int(time.time()))[:6]}"
    cart = get_cart_data(request)['cart']
    
    domain = request.GET.get('domain')  # Provide a default domain
    total_amount = request.GET.get('total_amount')
    customer_name = request.GET.get('customer_name')
    customer_email = request.GET.get('customer_email')
    customer_address = request.GET.get('Customer Address')
    customer_phone = request.GET.get('customer_phone')
    shipping_fee = request.GET.get('shipping_fee')

    context = {
        "cart": cart,
        "total_amount": total_amount,
        "customer_name": customer_name,
        "customer_email": customer_email,
        "customer_address": customer_address,
        "customer_phone": customer_phone,
        "shipping_fee": shipping_fee,
    }
    
    order_id = create_order(request, 'SSLCommerz', context)
    create_payment_data(request, 'SSLCommerz', transaction_id, total_amount)

    params = urlencode({'order_id': order_id, 'transaction_id': transaction_id})
    success_url = f'http://{domain}/payment/success/?{params}'
    fail_url = f'http://{domain}/payment/fail/?{params}'
    cancel_url = f'http://{domain}/payment/cancel/?{params}'

    if not all([total_amount, customer_name, customer_email, customer_address, customer_phone]):
        return HttpResponseBadRequest("Missing required parameters")
    

    payment_data = {
        "store_id": settings.SSL_COMMERZ_STORE_ID,
        "store_passwd": settings.SSL_COMMERZ_STORE_PASSWORD,
        "total_amount": total_amount,
        "currency": "BDT",
        "tran_id": transaction_id,
        "success_url": success_url,
        "fail_url": fail_url,
        "cancel_url": cancel_url,
        "cus_name": customer_name,
        "cus_email": customer_email,
        "cus_add1": customer_address,
        "cus_city": "Dhaka",
        "cus_country": "Bangladesh",
        "shipping_method": "NO",
        "cus_phone": customer_phone,
        'num_of_item': len(cart.items.all()), 
        'product_name': ", ".join(p.product.name for p in cart.items.all()),
        'product_category': ", ".join(p.product.category.name for p in cart.items.all()), 
        'product_profile': "general",
    } 
    
    cart.items.all().delete()

    # Initialize SSLCOMMERZ
    sslcommerz = SSLCOMMERZ({
        'store_id': settings.SSL_COMMERZ_STORE_ID,
        'store_pass': settings.SSL_COMMERZ_STORE_PASSWORD,
        'issandbox': True if settings.DEBUG else False
    })
    # Create payment session
    try:
        response = sslcommerz.createSession(payment_data)

        # Check if GatewayPageURL is present and valid
        if 'GatewayPageURL' not in response or not response['GatewayPageURL']:
            error_message = response.get('failedreason', 'Payment gateway URL not found. Please try again.')
            return HttpResponse(f"Error: {error_message}", status=500)

        # Redirect to the payment gateway
        return redirect(response['GatewayPageURL'])

    except Exception as e:
        # Handle any exceptions during API call
        return HttpResponse(f"An error occurred: {str(e)}", status=500)
    
def sslcommerz_retry_payment(request):
    order_id=request.GET.get('order_id')
    old_transaction_id = request.GET.get('transaction_id')
    customer_id = Customer.objects.get(user = request.user).id
    transaction_id = f"TNX-{str(uuid.uuid4())[:4]}-00{customer_id}-{str(int(time.time()))[:6]}"
    order = get_object_or_404(Order, order_id=order_id)
    
    create_payment_data(request, 'SSLCommerz', transaction_id, order.total)

    params = urlencode({'order_id': order_id, 'transaction_id': transaction_id})
    success_url = f'http://{request.get_host()}/payment/success/?{params}'
    fail_url = f'http://{request.get_host()}/payment/fail/?{params}'
    cancel_url = f'http://{request.get_host()}/payment/cancel/?{params}'

    payment_data = {
        "store_id": settings.SSL_COMMERZ_STORE_ID,
        "store_passwd": settings.SSL_COMMERZ_STORE_PASSWORD,
        "total_amount": order.total,
        "currency": "BDT",
        "tran_id": transaction_id,
        "success_url": success_url,
        "fail_url": fail_url,
        "cancel_url": cancel_url,
        "cus_name": order.customer_name,
        "cus_email": order.email,
        "cus_add1": order.shipping_address,
        "cus_city": "Dhaka",
        "cus_country": "Bangladesh",
        "shipping_method": "NO",
        "cus_phone": order.customer_phone,
        'num_of_item': len(order.items.all()), 
        'product_name': ", ".join(p.product.name for p in order.items.all()),
        'product_category': ", ".join(p.product.category.name for p in order.items.all()), 
        'product_profile': "general",
    } 
    if old_transaction_id:
        try:
            old_payment = get_object_or_404(Payment, transaction_id=old_transaction_id)
            if  not old_payment.status == 'completed':
                old_payment.delete()
        except Exception:
            pass

    # Initialize SSLCOMMERZ
    sslcommerz = SSLCOMMERZ({
        'store_id': settings.SSL_COMMERZ_STORE_ID,
        'store_pass': settings.SSL_COMMERZ_STORE_PASSWORD,
        'issandbox': True if settings.DEBUG else False
    })
    # Create payment session
    try:
        response = sslcommerz.createSession(payment_data)

        # Check if GatewayPageURL is present and valid
        if 'GatewayPageURL' not in response or not response['GatewayPageURL']:
            error_message = response.get('failedreason', 'Payment gateway URL not found. Please try again.')
            return HttpResponse(f"Error: {error_message}", status=500)

        # Redirect to the payment gateway
        return redirect(response['GatewayPageURL'])

    except Exception as e:
        # Handle any exceptions during API call
        return HttpResponse(f"An error occurred: {str(e)}", status=500)


@csrf_exempt
def payment_success(request):
    transaction_id = request.GET.get('transaction_id')
    order_id = request.GET.get('order_id')
    order = get_object_or_404(Order, order_id=order_id)
    if transaction_id is not None:
        payment= get_object_or_404(Payment, transaction_id=transaction_id)
        payment.status='completed'
        payment.save()

    return render(request, 'payments/payment_success.html', {
        'transaction_id': transaction_id,
        'order': order,
        'order_items':order.items.all(),
        'total':order.total
    })


@csrf_exempt
def payment_fail(request):
    error_code = request.GET.get('error_code')
    print(error_code, 'this is error codeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee')
    order_id = request.GET.get('order_id')
    transaction_id = request.GET.get('transaction_id')
    order = get_object_or_404(Order, order_id=order_id)
    if transaction_id is not None:
        payment= get_object_or_404(Payment, transaction_id=transaction_id)
        payment.status='failed'
        payment.save()

    return render(request, 'payments/payment_fail.html', {
        'transaction_id': transaction_id,
        'order': order,
        'order_items':order.items.all(),
        'total':order.total
    })


@csrf_exempt
def payment_cancel(request):   
    order_id = request.GET.get('order_id')
    order = get_object_or_404(Order, order_id=order_id)
    transaction_id = request.GET.get('transaction_id')

    if transaction_id is not None:
        payment= get_object_or_404(Payment, transaction_id=transaction_id)
        payment.status='canceled'
        payment.save()

    return render(request, 'payments/payment_cancel.html', {
        'transaction_id': transaction_id,
        'order': order,
        'order_items':order.items.all(),
        'total':order.total
    })


def cash_on_delivery(request):
    domain = request.GET.get('domain')
    context = {
        "cart": get_cart_data(request)['cart'],
        "total_amount": request.GET.get('total_amount'),
        "customer_name": request.GET.get('customer_name'),
        "customer_email": request.GET.get('customer_email'),
        "customer_address": request.GET.get('Customer Address'),
        "customer_phone": request.GET.get('customer_phone'),
        "shipping_fee": request.GET.get('shipping_fee'),
    }
    
    order_id = create_order(request, 'cash_on_delivery', context)
    create_payment_data(request, 'SSLCommerz', None, context['total_amount'])

    context['cart'].items.all().delete()
    params = urlencode({'order_id': order_id})
    redirect_url = f'http://{domain}/payment/cash-on-delivery/success/?{params}'
    return redirect(redirect_url)


def create_payment_data(request, payment_method, transaction_id, amount):
    Payment.objects.create(
        user=request.user,
        payment_method=payment_method,
        transaction_id=transaction_id,
        amount=amount
    )
    