from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from .models import Product, Cart, CartItem
from accounts.models import Seller
from discounts.models import Coupon
from shipping.models import ShoppigData
from decimal import Decimal

def add_to_cart(request, product_slug, num_product):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'User not authenticated'}, status=401)
    
    product = get_object_or_404(Product, slug=product_slug)
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    cart_item.quantity += int(num_product)
    cart_item.save()

    return JsonResponse({'status': 'success', 'message': 'Product added to cart'})


def get_cart_data(request):
    cart = get_object_or_404(Cart, user=request.user)
    products = cart.items.all().values_list('product', flat=True)
    sellers = Seller.objects.filter(products__in=products).distinct()
    shipping_address, created = ShoppigData.objects.get_or_create(user=request.user)
    if cart.get_total_item_count() == 0:
        shipping_fee = Decimal(0)
    elif shipping_address.district == "Dhaka":
        shipping_fee = Decimal(60)
    elif shipping_address.division == shipping_address.district:
        shipping_fee = Decimal(80)
    else:
        shipping_fee = Decimal(110)
    shipping_fee = shipping_fee * len(sellers)
    total = cart.get_total_price() - cart.get_discount() + shipping_fee
    domain = request.get_host()
    
    return {
        "cart": cart,
        "total": total,
        "shipping_fee": shipping_fee,
        "domain": domain,
        "shipping": shipping_address,
    }

def cart_view(request):
    context = get_cart_data(request)
    cart = context['cart']
    if request.method == "POST":
        for item in cart.items.all():
            new_quantity = request.POST.get(f'num-product{item.id}')
            if new_quantity and new_quantity.isdigit() and int(new_quantity) != item.quantity:
                CartItem.objects.filter(id=item.id).update(quantity=new_quantity)
    
    return render(request, 'cart/shoping-cart.html', context)


def update_cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    shipping_fee = Decimal(70)
    total = cart.get_total_price() - cart.get_discount() - shipping_fee
    domain = request.get_host()
    return render(request, 'cart/shoping-cart.html',{
        "cart":cart,
        "total":total,
        "domain":domain,
    })