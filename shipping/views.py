from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ShoppigData
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
    
