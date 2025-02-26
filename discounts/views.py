from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from discounts.models import Coupon
from cart.models import Cart


def coupon_apply(request, cart_id, coupon_code,):
    coupon = coupon_code
    if not coupon_code:
        return JsonResponse({"detail": "Coupon code is required."}, status=400)
    try:
        coupon = Coupon.objects.get(code=coupon_code)
    except Coupon.DoesNotExist:
        return JsonResponse({"detail": "Invalid coupon code."}, status=400)
    cart = get_object_or_404(Cart, id=cart_id)
    if not cart:
        return JsonResponse({"detail": "User cart not found."}, status=400)
        
    cart.coupon = coupon
    cart.save()
    return JsonResponse({"detail": "Coupon applied successfully."}, status=200)