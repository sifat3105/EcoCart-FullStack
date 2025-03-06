from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.core.paginator import Paginator 
from products.views import all_product_views, Category
import requests
from django.http import JsonResponse
from django.utils.text import slugify
import uuid
from products.models import Product, Seller, Category

def fetch_and_create_products(request):
    url = "https://dummyjson.com/products"  
    response = requests.get(url)

    if response.status_code != 200:
        return JsonResponse({"error": "Failed to fetch products from dummyjson.com"}, status=400)

    products_data = response.json().get('products', [])
    created_products = []
    updated_products = []

    for product_data in products_data:
        # Assuming you have a default Seller and Category for simplicity
        seller, _ = Seller.objects.get_or_create(user=request.user)
        category, _ = Category.objects.get_or_create(name=product_data['category'])

        # Create or update the Product
        product, created = Product.objects.update_or_create(
            sku=product_data.get('id'),
            defaults={
                'seller': seller,
                'uuid': uuid.uuid4(),
                'slug': slugify(product_data['title']),
                'name': product_data['title'],
                'category': category,
                'short_description': product_data.get('description', '')[:255],
                'description': product_data.get('description', ''),
                'price': product_data['price'],
                'stock': product_data.get('stock', 0),
                'image_url': product_data.get('thumbnail', ''),
                'weight': product_data.get('weight', None),
                'dimensions': f"{product_data.get('height', 0)}x{product_data.get('width', 0)}x{product_data.get('length', 0)}",
                'materials': product_data.get('material', ''),
                'color': product_data.get('color', ''),
                'size': product_data.get('size', ''),
                'brand': product_data.get('brand', ''),
                'rating': product_data.get('rating', 0),
                'discountPercentage': product_data.get('discountPercentage', 0),
            }
        )

        if created:
            created_products.append(product.name)
        else:
            updated_products.append(product.name)

    return JsonResponse({
        "message": "Products fetched and processed successfully",
        "created_products": created_products,
        "updated_products": updated_products,
    })



def home_views(request):
    # fetch_and_create_products(request)
    all_products= all_product_views(request)[:10]
    total_products = Product.objects.all().count()

    return render(request, 'home/index.html',{
        'product_list': all_products,
        'total_products': total_products
    })


def quick_view(request, product_slug):
    print("Quick view for product:", product_slug)
    product = get_object_or_404(Product, slug=product_slug)
    data = {
        'name': product.name,
        'price': product.price,
        'image': product.get_image(),
        'description': product.short_description,
    }
    return JsonResponse(data)

def load_more(request):
    offset = int(request.GET.get('offset', 0))
    limit = int(request.GET.get('limit', 10))
    all_products= all_product_views(request)[offset:offset+limit]
    total_products = Product.objects.all().count()

    data= render_to_string('product/partials/product_list.html', {'product_list': all_products})
    return JsonResponse({
        'data': data
    })