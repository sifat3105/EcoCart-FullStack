from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse
from .models import Product, ProductImage, Category
from accounts.models import Seller
from django.db.models import Q
from urllib.parse import urlencode
import random
import string

def all_product_views(request):
    products = Product.objects.all()
    
    product_list = []
    if products:
        for product in products:
            images = product.images.all()
            product_list.append({
                'product': product,
                'images': images
            })
    
    return product_list

def create_product_views(request):
    if request.method == 'POST':
        # Handle Product creation
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        short_description = request.POST.get('short_description')
        description = request.POST.get('description')
        price = request.POST.get('price')
        discounted_price = request.POST.get('discounted_price')
        stock = request.POST.get('stock')
        weight = request.POST.get('weight')
        dimensions = request.POST.get('dimensions')
        materials = request.POST.get('materials')
        color = request.POST.get('color')
        size = request.POST.get('size')
        image = request.FILES.get('image')

        # Get the category instance
        category = Category.objects.get(id=category_id)

        # Create the product
        product = Product(
            seller=request.user.seller, 
            name=name,
            category=category,
            short_description=short_description,
            description=description,
            price=price,
            discounted_price=discounted_price,
            stock=stock,
            image=image,
            weight=weight,
            dimensions=dimensions,
            materials=materials,
            color=color,
            size=size
        )
        product.save()

        images = request.FILES.getlist('images')
        for img in images:
            ProductImage.objects.create(product=product, image=img)

        return redirect('product_detail', slug=product.slug)

    categories = Category.objects.all()
    return render(request, 'product/create_product.html', {'categories': categories})



def product_detail(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    images = ProductImage.objects.filter(product=product)
    domain = request.get_host()
    return render(request ,"product/product_detail.html", {"product": product, "images": images, "domain": domain})





def product_list_view(request):
    products = Product.objects.all()

    # Filtering Logic
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(materials__icontains=search_query) |
            Q(size__icontains=search_query)
        )

    price_range = request.GET.get('price', '')
    if price_range:
        price_mapping = {
            "$0.00 - $50.00": (0, 50),
            "$50.00 - $100.00": (50, 100),
            "$100.00 - $150.00": (100, 150),
            "$150.00 - $200.00": (150, 200),
            "$200.00+": (200, None),
        }
        min_price, max_price = price_mapping.get(price_range, (None, None))
        if min_price is not None:
            products = products.filter(price__gte=min_price)
        if max_price is not None:
            products = products.filter(price__lte=max_price)

    color = request.GET.get('color', '')
    if color:
        products = products.filter(color__iexact=color)

    category = request.GET.get('category', '')
    if category:
        products = products.filter(category__name__iexact=category)

    size = request.GET.get('size', '')
    if size:
        products = products.filter(size__icontains=size)

    material = request.GET.get('material', '')
    if material:
        products = products.filter(materials__icontains=material)

    sort_by = request.GET.get('sort', '')
    sort_options = {
        "popularity": "-stock",
        "average_rating": "-updated_at",
        "newness": "-created_at",
        "price_low_to_high": "price",
        "price_high_to_low": "-price"
    }
    if sort_by in sort_options:
        products = products.order_by(sort_options[sort_by])

    # Check if it's an AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, "product/partials/product_list.html", {"products": products})

    return render(request, "product/products.html", {"products": products})


def product_search(request):
    query = request.GET.get('q', '')

    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()  # Show all if no query
    categories = Category.objects.filter(products__in=products).distinct()
    context = {
        'products': products,
        'query': query,
        "categories":categories
    }
    
    return render(request, 'product/products.html', context)

def generate_random_string(length=10):
    """Generate a random string for query parameters like 'spm'."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def search_redirect(request):
    print(request.GET)
    query = request.GET.get('q', '').strip()  # Get search query and remove extra spaces
    
    if not query:
        return HttpResponseRedirect(reverse('product_search'))  # Redirect to search page if empty

    # Save search history in session
    search_history = request.session.get('search_history', [])  # Retrieve previous searches
    if query not in search_history:  # Avoid duplicates
        search_history.insert(0, query)  # Add new search to the beginning
        if len(search_history) > 10:  # Keep only the last 10 searches
            search_history.pop()
        request.session['search_history'] = search_history  # Save back to session

    # Generate dynamic parameters
    spm = f"a2a0e.tm{random.randint(100000, 999999)}.search.{random.randint(1, 5)}.{generate_random_string(10)}"
    keyori = random.choice(["ss", "search_suggestion", "history"])
    search_from = random.choice(["search_history", "homepage_suggestion", "category_recommendation"])
    sugg = f"{query}_0_{random.randint(1, 10)}"

    # Construct query parameters dynamically
    params = {
        "spm": spm,
        "q": query,
        "_keyori": keyori,
        "from": search_from,
        "sugg": sugg
    }

    # Encode parameters into URL
    query_string = urlencode(params)

    # Redirect to product search page with query parameters
    return HttpResponseRedirect(f"{reverse('product_search')}?{query_string}")


def quick_view(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    images = ProductImage.objects.filter(product=product)

    context = {
        "product": product,
        "images": images,
    }

    model_html = render_to_string('product/partials/quick_view_image.html', context)
    context.clear()
    data = {
        "model_html": model_html
    }
    return JsonResponse(data)