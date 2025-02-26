from django.urls import path
from .views import move_to_cart, remove_from_wishlist, wishlist_view

urlpatterns = [
    path('wishlist/', wishlist_view, name="name" ),
    path('wishlist/move-to-cart/<int:item_id>/', move_to_cart, name='move_to_cart'),
    path('wishlist/remove/<int:item_id>/', remove_from_wishlist, name='remove_from_wishlist'),
]