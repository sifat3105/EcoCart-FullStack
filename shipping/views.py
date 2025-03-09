from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import Order, ShippingUpdate, ShoppigData
import json

@csrf_exempt  
def update_shipping(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body)
            division = data.get('division')
            district = data.get('district')
            upazila = data.get('upazila')
            address = data.get('address')
            number = data.get('number')
            print(division, district, upazila, address, number
            )

            if not all([division, district, upazila, address, number]):
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            shipping, created = ShoppigData.objects.get_or_create(user=request.user)
            shipping.division = str(division)
            shipping.district = str(district)
            shipping.upazila = str(upazila)
            shipping.address = str(address)
            shipping.number = str(number)
            shipping.save()
            print('Shippingg Address successfully')
            # Return a success response
            return JsonResponse({'status': 'success', 'message': 'Shippingg Address update successfully'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
    




def add_shipping_update(request, order_id=None):
    # Get all orders that are not delivered
    orders = Order.objects.exclude(status='Delivered')

    if order_id:
        # Get the specific order object
        order = get_object_or_404(Order, order_id=order_id)

        if request.method == 'POST':
            # Get data from the POST request
            status = request.POST.get('status')
            description = request.POST.get('description', '')

            # Create a new ShippingUpdate object
            ShippingUpdate.objects.create(
                order=order,
                status=status,
                description=description,
                timestamp=timezone.now()  # Automatically set the current timestamp
            )

            # Redirect to the track order page or back to the add shipping update page
            # return redirect('add_shipping_update')

        # Render the update form for GET requests
        return render(request, 'shipping/add_shipping_update.html', {
            'orders': orders,
            'selected_order': order,
        })

    # Render the page with the list of orders if no order_id is provided
    return render(request, 'shipping/add_shipping_update.html', {
        'orders': orders,
        'selected_order': None,
    })
    
