from django.shortcuts import render , get_object_or_404
from products.models import Category, Product
from accounts.models import Seller
from .models import Order, OrderItems, SellerOrder, SellerOrderItems
from shipping.models import ShippingUpdate
from decimal import Decimal
import uuid
import logging
from django.db import transaction
from django.core.exceptions import ValidationError



logger = logging.getLogger(__name__)

def create_order(request, payment_method, context):
    try:
        # Validate context
        required_keys = ['cart', 'total_amount', 'customer_name', 'customer_email', 'customer_address', 'customer_phone', 'shipping_fee']
        for key in required_keys:
            if key not in context:
                raise ValidationError(f"Missing required key in context: {key}")

        with transaction.atomic():
            id = Order.objects.count() + 999999
            order_id = f"ODR-{id}"
           
            cart = context['cart']
            total = Decimal(context['total_amount'])
            customer_name = context['customer_name']
            customer_email = context['customer_email']
            customer_address = context['customer_address']
            customer_phone = context['customer_phone']
            shipping_fee = Decimal(context['shipping_fee'])

            cart_items = cart.items.all()

            order = Order.objects.create(
                user = request.user,
                email=customer_email,
                order_id=order_id,
                payment_method=payment_method,
                customer_name=customer_name,
                customer_phone=customer_phone,
                shipping_address=customer_address,
                subtotal=total - shipping_fee,
                shipping_fee=shipping_fee,
                total=total,
            )

            for item in cart_items:
                OrderItems.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price,
                )
           
            logger.info(f"Order created successfully: {order_id}")
            
            create_seller_order(order_id)
            return order_id

    except Exception as e:
        logger.error(f"Error creating order: {e}")
        raise


def create_seller_order(order_id):
    try:
        order = Order.objects.get(order_id=order_id)
        products_id = order.items.all().values_list('product', flat=True)
        product_list = Product.objects.filter(id__in=products_id)
        print(product_list)
        sellers = Seller.objects.filter(products__in=products_id).distinct()
        print(sellers)
        for seller in sellers:
            seller_products = product_list.filter(seller=seller)
            total = sum([item.product.price * item.quantity for item in order.items.all() if item.product in seller_products])
            seller_order = SellerOrder.objects.create(
                order=order,
                seller=seller,
                total=total,
            )
            for seller_product in seller_products:
                item = order.items.get(product=seller_product)
                SellerOrderItems.objects.create(
                    order=seller_order,
                    product=seller_product,
                    quantity=item.quantity,
                    price=seller_product.price,
                )
            logger.info(f"Seller order created successfully for {seller.user.username}")
        return
    except Exception as e:  
        logger.error(f"Error creating seller order: {e}")
        raise


def order_details(reqest):
    order_id=reqest.GET.get('order_id')
    order = get_object_or_404(Order, order_id=order_id)
    return render(reqest, 'order/order_details.html',{
        'order':order,
        'uuid':uuid.uuid4()
    })

def tack_order(reqest):
    order_id=reqest.GET.get('order_id')
    order = get_object_or_404(Order, order_id=order_id)
    shipping_updates = ShippingUpdate.objects.filter(order=order).order_by('-timestamp') 
    return render(reqest, 'order/track_order.html',{
        'order':order,
        'shipping_updates':shipping_updates
        
    })