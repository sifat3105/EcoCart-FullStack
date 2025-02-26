from django.shortcuts import redirect, get_object_or_404, render
from cart.models import Cart
from .models import Wishlist, WishlistItem

def wishlist_view(request):
    wishlist = Wishlist.objects.get(user=request.user)  # Fetch the wishlist for the logged-in user
    return render(request, 'wishlist.html', {'wishlist': wishlist})



def move_to_cart(request, item_id):
    wishlist_item = get_object_or_404(WishlistItem, id=item_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart.items.add(wishlist_item.product)
    wishlist_item.delete()
    return redirect('wishlist')

def remove_from_wishlist(request, item_id):
    wishlist_item = get_object_or_404(WishlistItem, id=item_id)
    wishlist_item.delete()
    return redirect('wishlist')